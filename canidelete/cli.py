#!/usr/bin/env python3
"""canidelete - find the workarounds in your code that you can finally delete.

Tag a workaround with a tripwire comment (see README) and canidelete tells you
when its reason to exist is gone: the upstream issue closed, the PR merged,
the dependency got upgraded, or the deadline passed.

Zero dependencies. Python 3.8+.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

__version__ = "0.1.0"

YES, WONTFIX, UNKNOWN, NO = "yes", "wontfix", "unknown", "no"
ORDER = {YES: 0, WONTFIX: 1, UNKNOWN: 2, NO: 3}

GH_LINK = re.compile(r"https?://github\.com/([\w.-]+)/([\w.-]+)/(issues|pull)/(\d+)")
MARKER = re.compile(
    r"(?:\b(?:REMOVE|DELETE|DROP)[-_](?:WHEN|AFTER|IF)\s*[:=]|(?<![\"'`\w])canidelete\s*:)\s*(.+)",
    re.I,
)
IGNORE = re.compile(r"canidelete\s*:\s*ignore\b(?!-)", re.I)
IGNORE_FILE = re.compile(r"canidelete\s*:\s*ignore-file", re.I)
SPLIT = re.compile(r"\s*(?:,|;|&&)\s*|\s+and\s+", re.I)
DATE = re.compile(r"^(?:>=\s*)?(\d{4}-\d{2}-\d{2})$")
VSPEC = re.compile(
    r"^(?:(npm|pypi|py|pip|node):)?(@?[\w.\-/]+?)\s*(>=|<=|==|!=|~=|>|<)\s*v?([\w.+\-]+)$", re.I
)
CLOSERS = re.compile(r"\s*(\*/|-->|#}|%>|\*\)|-})\s*$")

SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".tgz",
    ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mp3", ".lock", ".map", ".svg",
}
SKIP_NAMES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "uv.lock", "Cargo.lock"}
DOC_EXT = {".md", ".markdown", ".rst", ".adoc", ".txt"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".tox", "target", "vendor"}


# --------------------------------------------------------------------------- data

@dataclass
class Condition:
    text: str
    kind: str = "unknown"
    status: str = UNKNOWN
    detail: str = ""


@dataclass
class Finding:
    file: str
    line: int
    source: str
    conditions: List[Condition] = field(default_factory=list)

    @property
    def status(self) -> str:
        """All conditions must be met (AND). Any 'not yet' blocks deletion."""
        states = {c.status for c in self.conditions}
        for s in (NO, WONTFIX, UNKNOWN):
            if s in states:
                return s
        return YES if states else UNKNOWN

    def to_dict(self) -> dict:
        return {
            "file": self.file, "line": self.line, "status": self.status, "source": self.source,
            "conditions": [dict(c.__dict__) for c in self.conditions],
        }


# --------------------------------------------------------------------------- versions

def _vkey(v: str) -> list:
    out = []
    for part in re.split(r"[.+\-_]", v.strip().lstrip("vV")):
        if not part:
            continue
        m = re.match(r"(\d+)(.*)", part)
        if m:
            out.append((int(m.group(1)), 0 if m.group(2) else 1, m.group(2)))
        else:
            out.append((-1, 0, part))  # pre-release words (rc, beta) sort before releases
    return out


def vcmp(a: str, b: str) -> int:
    ka, kb = _vkey(a), _vkey(b)
    n = max(len(ka), len(kb))
    ka += [(0, 1, "")] * (n - len(ka))
    kb += [(0, 1, "")] * (n - len(kb))
    return (ka > kb) - (ka < kb)


def satisfies(have: str, op: str, want: str) -> bool:
    c = vcmp(have, want)
    return {">=": c >= 0, "~=": c >= 0, ">": c > 0, "<=": c <= 0, "<": c < 0,
            "==": c == 0, "!=": c != 0}[op]


def _norm_py(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


class Versions:
    """Resolves a dependency's version from lockfiles / installed packages in the repo."""

    def __init__(self, root: str):
        self.root = root
        self._cache: Dict[Tuple[str, str], Tuple[Optional[str], str]] = {}
        self._files: Dict[str, Optional[str]] = {}

    def _read(self, rel: str) -> Optional[str]:
        if rel not in self._files:
            try:
                with open(os.path.join(self.root, rel), encoding="utf-8", errors="replace") as f:
                    self._files[rel] = f.read()
            except OSError:
                self._files[rel] = None
        return self._files[rel]

    def get(self, eco: Optional[str], name: str) -> Tuple[Optional[str], str]:
        key = ((eco or "").lower(), name.lower())
        if key not in self._cache:
            self._cache[key] = self._lookup(key[0], name)
        return self._cache[key]

    def _lookup(self, eco: str, name: str) -> Tuple[Optional[str], str]:
        low = name.lower()
        if not eco and low in ("python", "cpython"):
            return platform.python_version(), "running interpreter"
        if not eco and low in ("node", "nodejs"):
            try:
                out = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10)
                if out.returncode == 0:
                    return out.stdout.strip().lstrip("v"), "node --version"
            except (OSError, subprocess.SubprocessError):
                pass
            return None, "node not found"
        if eco in ("", "npm", "node"):
            v = self._npm(name)
            if v[0]:
                return v
        if eco in ("", "pypi", "py", "pip"):
            v = self._py(name)
            if v[0]:
                return v
        return None, "not found in lockfiles or installed packages"

    def _npm(self, name: str) -> Tuple[Optional[str], str]:
        pj = self._read(os.path.join("node_modules", name, "package.json"))
        if pj:
            try:
                return json.loads(pj)["version"], "node_modules"
            except (ValueError, KeyError):
                pass
        lock = self._read("package-lock.json")
        if lock:
            try:
                data = json.loads(lock)
                pkg = (data.get("packages", {}).get("node_modules/" + name)
                       or data.get("dependencies", {}).get(name))
                if pkg and pkg.get("version"):
                    return pkg["version"], "package-lock.json"
            except ValueError:
                pass
        yarn = self._read("yarn.lock")
        if yarn:
            m = re.search(r'(?m)^"?' + re.escape(name)
                          + r'@[^\n]*:\n(?:[ \t]+.*\n)*?[ \t]+version:?\s+"?([^"\s]+)', yarn)
            if m:
                return m.group(1), "yarn.lock"
        pnpm = self._read("pnpm-lock.yaml")
        if pnpm:
            m = re.search(r"(?m)^\s+'?/?" + re.escape(name) + r"[@/](\d[\w.\-+]*)", pnpm)
            if m:
                return m.group(1), "pnpm-lock.yaml"
        return None, ""

    def _py(self, name: str) -> Tuple[Optional[str], str]:
        want = _norm_py(name)
        for lock in ("uv.lock", "poetry.lock", "pdm.lock"):
            text = self._read(lock)
            if text:
                for m in re.finditer(r'(?m)^name\s*=\s*"([^"]+)"\s*\n\s*version\s*=\s*"([^"]+)"', text):
                    if _norm_py(m.group(1)) == want:
                        return m.group(2), lock
        try:
            reqs = sorted(f for f in os.listdir(self.root) if re.match(r"requirements.*\.txt$", f))
        except OSError:
            reqs = []
        for req in reqs:
            for line in (self._read(req) or "").splitlines():
                m = re.match(r"\s*([\w.\-]+)(?:\[.*?\])?\s*==\s*([\w.+\-]+)", line)
                if m and _norm_py(m.group(1)) == want:
                    return m.group(2), req
        try:
            from importlib import metadata
            return metadata.version(name), "installed"
        except Exception:
            return None, ""


# --------------------------------------------------------------------------- github

def _token(explicit: Optional[str]) -> Optional[str]:
    tok = explicit or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok
    try:
        out = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return None


def fetch_github(owner: str, repo: str, num: str, token: Optional[str]) -> dict:
    url = "https://api.github.com/repos/%s/%s/issues/%s" % (owner, repo, num)
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "canidelete/" + __version__,
    })
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"_error": "not found (private repo? set GITHUB_TOKEN)"}
        if e.code in (403, 429):
            return {"_error": "GitHub rate limit hit - set GITHUB_TOKEN"}
        return {"_error": "GitHub returned HTTP %d" % e.code}
    except Exception as e:  # network down, DNS, timeout...
        return {"_error": "network error: %s" % e.__class__.__name__}


def ago(iso: Optional[str], now: Optional[dt.datetime] = None) -> str:
    if not iso:
        return ""
    try:
        then = dt.datetime.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return ""
    now = now or dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    days = (now - then).days
    if days < 1:
        return "today"
    if days < 60:
        return "%dd ago" % days
    if days < 730:
        return "%dmo ago" % (days // 30)
    return "%dy %dmo ago" % (days // 365, (days % 365) // 30)


def judge_github(data: dict) -> Tuple[str, str]:
    if "_error" in data:
        return UNKNOWN, data["_error"]
    title = (data.get("title") or "").strip()
    if len(title) > 60:
        title = title[:57] + "..."
    title = ' "%s"' % title if title else ""
    pr = data.get("pull_request")
    if data.get("state") == "open":
        return NO, ("PR still open" if pr else "issue still open") + title
    when = ago(data.get("closed_at"))
    if pr:
        if pr.get("merged_at"):
            return YES, "PR merged %s%s" % (ago(pr["merged_at"]), title)
        return WONTFIX, "PR closed without merging %s%s" % (when, title)
    if data.get("state_reason") == "not_planned":
        return WONTFIX, "closed as not planned %s, the workaround may be permanent%s" % (when, title)
    return YES, "closed %s%s" % (when, title)


# --------------------------------------------------------------------------- scanning

def list_files(root: str, paths: List[str]) -> List[str]:
    try:
        out = subprocess.run(
            ["git", "-C", root, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", *paths],
            capture_output=True, check=True, timeout=60,
        ).stdout.decode("utf-8", "replace")
        files = [f for f in out.split("\0") if f]
        return [f for f in files if os.path.isfile(os.path.join(root, f))]
    except (OSError, subprocess.SubprocessError):
        pass
    files = []
    for base in (paths or ["."]):
        full = os.path.join(root, base)
        if os.path.isfile(full):
            files.append(os.path.normpath(base))
            continue
        for d, dirs, names in os.walk(full):
            dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("."))
            for n in sorted(names):
                files.append(os.path.relpath(os.path.join(d, n), root))
    return files


def parse_condition(text: str) -> Condition:
    text = text.strip().strip("`'\"").rstrip(".")
    c = Condition(text=text)
    if GH_LINK.search(text):
        c.kind = "github"
    elif DATE.match(text):
        c.kind = "date"
    elif VSPEC.match(text):
        c.kind = "version"
    else:
        c.detail = "can't parse this (try pkg>=1.2, 2026-01-31 or a GitHub issue/PR URL)"
    return c


def scan_line(line: str, bare_links: bool = True) -> Optional[List[Condition]]:
    if IGNORE.search(line):
        return None
    m = MARKER.search(line)
    if m:
        body = m.group(1)
        while True:
            stripped = CLOSERS.sub("", body)
            if stripped == body:
                break
            body = stripped
        conds = [parse_condition(p) for p in SPLIT.split(body) if p and p.strip()]
        return conds or None
    if bare_links:
        links = GH_LINK.findall(line)
        if links:
            seen, conds = set(), []
            for l in links:
                url = "https://github.com/%s/%s/%s/%s" % l
                if url not in seen:
                    seen.add(url)
                    conds.append(Condition(text=url, kind="github"))
            return conds
    return None


def scan(root: str, paths: Optional[List[str]] = None, include_docs: bool = False,
         bare_links: bool = True) -> List[Finding]:
    findings = []
    for rel in list_files(root, paths or []):
        norm = rel.replace("\\", "/")
        base = os.path.basename(norm)
        ext = os.path.splitext(base)[1].lower()
        if ext in SKIP_EXT or base in SKIP_NAMES or base.endswith((".min.js", ".min.css")):
            continue
        if any(part in SKIP_DIRS for part in norm.split("/")[:-1]):
            continue
        is_doc = ext in DOC_EXT or base.upper().startswith(("CHANGELOG", "CHANGES", "HISTORY", "NEWS"))
        if is_doc and not include_docs:
            continue
        full = os.path.join(root, rel)
        try:
            if os.path.getsize(full) > 2_000_000:
                continue
            with open(full, "rb") as f:
                raw = f.read()
        except OSError:
            continue
        if b"\0" in raw[:8000]:
            continue
        text = raw.decode("utf-8", "replace")
        if IGNORE_FILE.search(text):
            continue
        if "github.com" not in text and not re.search(r"(?i)(remove|delete|drop)[-_]|canidelete", text):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            conds = scan_line(line, bare_links=bare_links)
            if conds:
                findings.append(Finding(file=norm, line=i, source=line.strip()[:200], conditions=conds))
    return findings


def evaluate(findings: List[Finding], root: str, offline: bool = False, token: Optional[str] = None,
             today: Optional[dt.date] = None, fetch=fetch_github) -> None:
    today = today or dt.date.today()
    versions = Versions(root)

    # fetch each unique GitHub reference exactly once, in parallel
    refs: Dict[tuple, Optional[dict]] = {}
    for f in findings:
        for c in f.conditions:
            if c.kind == "github":
                m = GH_LINK.search(c.text)
                refs[(m.group(1).lower(), m.group(2).lower(), m.group(4))] = None
    if refs and not offline:
        tok = _token(token)
        keys = list(refs)
        with ThreadPoolExecutor(max_workers=8) as pool:
            for k, data in zip(keys, pool.map(lambda k: fetch(k[0], k[1], k[2], tok), keys)):
                refs[k] = data

    for f in findings:
        for c in f.conditions:
            if c.kind == "github":
                m = GH_LINK.search(c.text)
                data = refs.get((m.group(1).lower(), m.group(2).lower(), m.group(4)))
                if data is None:
                    c.status, c.detail = UNKNOWN, "skipped (--offline)"
                else:
                    c.status, c.detail = judge_github(data)
            elif c.kind == "date":
                try:
                    d = dt.date.fromisoformat(DATE.match(c.text).group(1))
                except ValueError:
                    c.status, c.detail = UNKNOWN, "invalid date"
                    continue
                if today >= d:
                    c.status = YES
                    c.detail = "deadline passed " + ("today" if today == d else "%d days ago" % (today - d).days)
                else:
                    c.status, c.detail = NO, "%d days to go" % (d - today).days
            elif c.kind == "version":
                eco, name, op, want = VSPEC.match(c.text).groups()
                have, where = versions.get(eco, name)
                if not have:
                    c.status, c.detail = UNKNOWN, "%s: %s" % (name, where or "version not found")
                elif satisfies(have, op, want):
                    c.status, c.detail = YES, "you have %s %s (%s)" % (name, have, where)
                else:
                    c.status, c.detail = NO, "you have %s %s (%s)" % (name, have, where)


# --------------------------------------------------------------------------- output

STYLE = {
    YES: ("✅", "DELETE IT", "32;1"),
    WONTFIX: ("\U0001faa6", "WON'T FIX", "35"),
    UNKNOWN: ("❓", "UNKNOWN", "33"),
    NO: ("⏳", "NOT YET", "2"),
}


def render(findings: List[Finding], color: bool = False, show_all: bool = False) -> str:
    def paint(s: str, code: str) -> str:
        return "\033[%sm%s\033[0m" % (code, s) if color else s

    out = []
    counts = {s: 0 for s in ORDER}
    for f in findings:
        counts[f.status] += 1
    shown = sorted(findings, key=lambda f: (ORDER[f.status], f.file, f.line))
    if not show_all:
        shown = [f for f in shown if f.status != NO]
    for f in shown:
        icon, label, code = STYLE[f.status]
        out.append("%s %s  %s" % (icon, paint(label.ljust(9), code), paint("%s:%d" % (f.file, f.line), "1")))
        for c in f.conditions:
            out.append("     %s %s  %s" % (STYLE[c.status][0], c.text, paint(c.detail, "2")))
    if out:
        out.append("")
    total = len(findings)
    if not total:
        out.append("No tripwires found. Tag a workaround with a REMOVE-WHEN comment to get started.")
    else:
        nfiles = len({f.file for f in findings})
        line = "%d tripwire%s in %d file%s: " % (total, "" if total == 1 else "s", nfiles, "" if nfiles == 1 else "s")
        line += ", ".join("%d %s" % (counts[s], STYLE[s][1].lower()) for s in ORDER if counts[s])
        out.append(line)
        if counts[YES]:
            n = counts[YES]
            out.append(paint("\U0001f5d1️  %d workaround%s can be deleted today." % (n, "" if n == 1 else "s"), "32;1"))
        if counts[NO] and not show_all:
            out.append(paint("(%d not-yet tripwires hidden, use --all to show them)" % counts[NO], "2"))
    return "\n".join(out)


HOME = "https://github.com/Telle-dev/canidelete"
COMMENT_MARK = "<!-- canidelete-report -->"
FOOTER = ("<sub>🗑️ Found by [canidelete](%s), the tool that tells you when a workaround can go. "
          "If it saved you time, a ⭐ helps others find it.</sub>" % HOME)


def _file_link(f: Finding) -> str:
    server, repo, sha = (os.environ.get(k) for k in ("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_SHA"))
    label = "`%s:%d`" % (f.file, f.line)
    if server and repo and sha:
        return "[%s](%s/%s/blob/%s/%s#L%d)" % (label, server, repo, sha, f.file, f.line)
    return label


def to_markdown(findings: List[Finding], footer: bool = True) -> str:
    rows = sorted((f for f in findings if f.status != NO), key=lambda f: (ORDER[f.status], f.file, f.line))
    n_yes = sum(1 for f in findings if f.status == YES)
    if n_yes:
        head = "### 🗑️ %d workaround%s can be deleted" % (n_yes, "" if n_yes == 1 else "s")
    else:
        head = "### ✅ No dead workarounds"
    out = [head, ""]
    if not rows:
        out.append("All %d tripwires are still waiting on something. Nothing to clean up." % len(findings))
    else:
        out += ["| | Location | Why |", "|---|---|---|"]
        for f in rows:
            why = "<br>".join("%s `%s` %s" % (STYLE[c.status][0], c.text.replace("|", "\\|"), c.detail.replace("|", "\\|"))
                              for c in f.conditions)
            out.append("| %s %s | %s | %s |" % (STYLE[f.status][0], STYLE[f.status][1], _file_link(f), why))
    if footer:
        out += ["", FOOTER]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- badge

def badge_svg(findings: List[Finding]) -> str:
    """shields-style badge: 'dead workarounds | N'."""
    n = sum(1 for f in findings if f.status == YES)
    label, value = "dead workarounds", str(n)
    color = "#3fb950" if n == 0 else ("#d29922" if n < 5 else "#e05d44")
    lw, vw = 6 * len(label) + 20, 7 * len(value) + 16
    w = lw + vw
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{l}: {v}">'
        '<title>{l}: {v} (canidelete)</title>'
        '<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/>'
        '<stop offset="1" stop-opacity=".1"/></linearGradient>'
        '<clipPath id="r"><rect width="{w}" height="20" rx="3" fill="#fff"/></clipPath>'
        '<g clip-path="url(#r)"><rect width="{lw}" height="20" fill="#555"/>'
        '<rect x="{lw}" width="{vw}" height="20" fill="{c}"/><rect width="{w}" height="20" fill="url(#s)"/></g>'
        '<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
        '<text x="{lx}" y="15" fill="#010101" fill-opacity=".3">{l}</text><text x="{lx}" y="14">{l}</text>'
        '<text x="{vx}" y="15" fill="#010101" fill-opacity=".3">{v}</text><text x="{vx}" y="14">{v}</text></g></svg>'
    ).format(w=w, lw=lw, vw=vw, c=color, l=label, v=value, lx=lw / 2, vx=lw + vw / 2)


# --------------------------------------------------------------------------- PR comments

def _gh_api(method: str, url: str, token: str, body: Optional[dict] = None) -> Tuple[int, object]:
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Accept": "application/vnd.github+json",
                                          "Authorization": "Bearer " + token,
                                          "User-Agent": "canidelete/" + __version__,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return 0, None


def comment_on_pr(findings: List[Finding], token: Optional[str], api=_gh_api) -> str:
    """Create or update one sticky comment on the current pull request.

    Posts only when something can be deleted; afterwards keeps that same comment
    up to date (including flipping it to 'all clear'). Never spams new comments.
    """
    event_path, repo = os.environ.get("GITHUB_EVENT_PATH"), os.environ.get("GITHUB_REPOSITORY")
    if not (event_path and repo and token):
        return "skipped: not running in a GitHub Actions pull_request job with a token"
    try:
        with open(event_path, encoding="utf-8") as fh:
            event = json.load(fh)
    except (OSError, ValueError):
        return "skipped: unreadable event payload"
    number = (event.get("pull_request") or {}).get("number")
    if not number:
        return "skipped: not a pull_request event"
    base = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    url = "%s/repos/%s/issues/%s/comments" % (base, repo, number)
    existing = None
    for page in range(1, 11):
        status, data = api("GET", "%s?per_page=100&page=%d" % (url, page), token)
        if status != 200 or not data:
            break
        existing = next((c for c in data if COMMENT_MARK in (c.get("body") or "")), existing)
        if len(data) < 100:
            break
    has_dead = any(f.status == YES for f in findings)
    if not existing and not has_dead:
        return "nothing to report"
    body = COMMENT_MARK + "\n" + to_markdown(findings)
    if existing:
        status, _ = api("PATCH", "%s/repos/%s/issues/comments/%s" % (base, repo, existing["id"]), token, {"body": body})
        return "updated comment" if status == 200 else "failed to update comment (HTTP %s)" % status
    status, _ = api("POST", url, token, {"body": body})
    if status == 201:
        return "posted comment"
    if status == 403:
        return "no permission to comment: add 'permissions: pull-requests: write' to the workflow"
    return "failed to post comment (HTTP %s)" % status


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="canidelete",
        description="Find the workarounds in your code that you can finally delete.",
    )
    p.add_argument("paths", nargs="*", help="files or directories to scan (default: whole repo)")
    p.add_argument("-C", "--root", default=".", help="project root (default: current directory)")
    p.add_argument("--check", action="store_true", help="exit 1 if anything can be deleted (for CI)")
    p.add_argument("--strict", action="store_true", help="with --check, also fail on won't-fix and unknown")
    p.add_argument("--offline", action="store_true", help="don't query GitHub")
    p.add_argument("--all", action="store_true", help="also list tripwires that haven't fired yet")
    p.add_argument("--markers-only", action="store_true",
                   help="only explicit REMOVE-WHEN markers, ignore bare GitHub links in comments")
    p.add_argument("--include-docs", action="store_true", help="also scan .md / .rst / CHANGELOG files")
    p.add_argument("--format", choices=("text", "json", "markdown"), default="text")
    p.add_argument("--json", action="store_const", const="json", dest="format", help="shorthand for --format json")
    p.add_argument("--token", help="GitHub token (default: $GITHUB_TOKEN, $GH_TOKEN or `gh auth token`)")
    p.add_argument("--badge", metavar="FILE", help="write a 'dead workarounds' SVG badge to FILE")
    p.add_argument("--comment-pr", action="store_true",
                   help="in a GitHub Actions pull_request job, post/update a sticky PR comment")
    p.add_argument("--no-color", action="store_true")
    p.add_argument("--version", action="version", version="canidelete " + __version__)
    a = p.parse_args(argv)

    root = os.path.abspath(a.root)
    findings = scan(root, a.paths, include_docs=a.include_docs, bare_links=not a.markers_only)
    evaluate(findings, root, offline=a.offline, token=a.token)

    if a.format == "json":
        print(json.dumps([f.to_dict() for f in findings], indent=2))
    elif a.format == "markdown":
        print(to_markdown(findings))
    else:
        color = sys.stdout.isatty() and not a.no_color and "NO_COLOR" not in os.environ
        try:
            print(render(findings, color, a.all))
        except UnicodeEncodeError:  # e.g. legacy Windows consoles
            print(render(findings, color, a.all).encode("ascii", "replace").decode())

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary and findings:
        try:
            with open(summary, "a", encoding="utf-8") as fh:
                fh.write(to_markdown(findings))
        except OSError:
            pass

    if a.badge:
        with open(a.badge, "w", encoding="utf-8") as fh:
            fh.write(badge_svg(findings))

    if a.comment_pr:
        print("[canidelete] " + comment_on_pr(findings, _token(a.token)), file=sys.stderr)

    if a.check:
        bad = {YES} | ({WONTFIX, UNKNOWN} if a.strict else set())
        return 1 if any(f.status in bad for f in findings) else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
