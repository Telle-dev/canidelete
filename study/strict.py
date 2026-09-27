#!/usr/bin/env python3
# canidelete: ignore-file
"""Stricter view of results.json: only comments that say they're a workaround / TODO / skip
and point at an issue or PR that's already resolved. Writes study/STRICT.md."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
WORDING = re.compile(r"(?i)\b(workaround|work around|hack|remove (this|it|when|once|after|if)|until\b|"
                     r"once .{0,40}\b(fixed|lands?|merged|released|resolved)|temporary|todo|fixme|xxx)\b|"
                     r"\.(skip|fixme)\(|\bskip\s*[:=]\s*true")
VENDORED = re.compile(r"(^|/)(assets|vendor|third_party|node_modules|__snapshots__|baselines|testdata/baselines)(/|$)|\.snap$")
AGE = re.compile(r"(?:(\d+)y )?(?:(\d+)mo )?(?:(\d+)d )?ago")


def age_days(detail):
    m = re.search(r"(\d+)y (\d+)mo ago|(\d+)mo ago|(\d+)d ago", detail)
    if not m:
        return 0
    if m.group(1):
        return int(m.group(1)) * 365 + int(m.group(2)) * 30
    if m.group(3):
        return int(m.group(3)) * 30
    return int(m.group(4))


def main():
    data = json.load(open(os.path.join(HERE, "results.json")))
    total = sum(len(v) for v in data.values())
    rows = []
    per_repo = {}
    for repo, findings in data.items():
        for f in findings:
            if f["status"] not in ("yes", "wontfix") or VENDORED.search(f["file"]):
                continue
            if not WORDING.search(f["source"]):
                continue
            c = f["conditions"][0]
            rows.append((age_days(c["detail"]), repo, f, c))
            per_repo[repo] = per_repo.get(repo, 0) + 1
    rows.sort(key=lambda r: -r[0])
    yes = [r for r in rows if r[2]["status"] == "yes"]
    wontfix = [r for r in rows if r[2]["status"] == "wontfix"]
    over_year = [r for r in yes if r[0] >= 365]

    out = [
        "# Workarounds waiting on bugs that are already closed", "",
        "canidelete found %d GitHub issue/PR links in code comments across 30 popular repos. Most of them are just "
        "references (a test pointing at the bug it covers, a \"see #123\" note), so this page only counts comments that "
        "**say** they're a workaround or a TODO: words like *workaround*, *hack*, *TODO*, *remove once*, *until*, or a "
        "skipped test." % total, "",
        "- **%d** of those point at an issue that's closed or a PR that's merged" % len(yes),
        "- **%d** of them were closed more than a year ago" % len(over_year),
        "- **%d** more point at issues closed as *not planned* or PRs closed without merging, so the workaround is "
        "probably permanent and the comment is misleading" % len(wontfix), "",
        "A closed issue doesn't always mean the workaround can go (the fix may be in a version the project doesn't use "
        "yet), but every one of these is worth a look.", "",
        "## Oldest ones", "",
    ]
    for days, repo, f, c in yes[:40]:
        url = "https://github.com/%s/blob/HEAD/%s#L%d" % (repo, f["file"], f["line"])
        src = f["source"].replace("|", "\\|")[:160]
        out.append("- **%s** [%s:%d](%s): %s  \n  `%s`" % (repo, f["file"], f["line"], url, c["detail"], src))
    out += ["", "## Per repo", "", "| Repo | Workaround comments on resolved issues |", "|---|---:|"]
    for repo, n in sorted(per_repo.items(), key=lambda kv: -kv[1]):
        out.append("| [%s](https://github.com/%s) | %d |" % (repo, repo, n))
    with open(os.path.join(HERE, "STRICT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(len(yes), "resolved,", len(over_year), "over a year,", len(wontfix), "wontfix")


if __name__ == "__main__":
    main()
