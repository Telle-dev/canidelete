#!/usr/bin/env python3
# canidelete: ignore-file
"""Run canidelete across famous open-source repos and build a leaderboard.

This is the launch hook: "We scanned 50 of the most popular repos on GitHub and
found N workarounds that can be deleted today."

    export GITHUB_TOKEN=ghp_...        # needed: thousands of issue lookups
    python study/run_study.py          # or: python study/run_study.py owner/repo ...

Writes study/RESULTS.md and study/results.json. Clones are shallow and cached in study/.repos.
"""
import json
import os
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from canidelete import cli  # noqa: E402

REPOS = """
facebook/react vercel/next.js microsoft/vscode microsoft/TypeScript nodejs/node
denoland/deno oven-sh/bun sveltejs/svelte vuejs/core angular/angular
django/django pallets/flask fastapi/fastapi psf/requests pandas-dev/pandas
numpy/numpy scikit-learn/scikit-learn pytorch/pytorch huggingface/transformers python/cpython
rust-lang/rust golang/go kubernetes/kubernetes moby/moby hashicorp/terraform
electron/electron vitejs/vite webpack/webpack babel/babel prettier/prettier
eslint/eslint jestjs/jest microsoft/playwright puppeteer/puppeteer tailwindlabs/tailwindcss
home-assistant/core ansible/ansible grafana/grafana prometheus/prometheus elastic/kibana
mastodon/mastodon discourse/discourse rails/rails laravel/framework godotengine/godot
neovim/neovim tensorflow/tensorflow apache/airflow langchain-ai/langchain sentry/sentry
""".split()


def run(repo):
    dest = os.path.join(HERE, ".repos", repo.replace("/", "__"))
    if not os.path.isdir(dest):
        subprocess.run(["git", "clone", "-q", "--depth", "1", "https://github.com/%s.git" % repo, dest], check=True)
    findings = cli.scan(dest)
    cli.evaluate(findings, dest)
    return findings


def main():
    if not os.environ.get("GITHUB_TOKEN"):
        sys.exit("Set GITHUB_TOKEN first (60 unauthenticated requests/hour won't cover this).")
    repos = sys.argv[1:] or REPOS
    rows, all_json = [], {}
    for i, repo in enumerate(repos, 1):
        print("[%d/%d] %s" % (i, len(repos), repo), file=sys.stderr)
        try:
            f = run(repo)
        except Exception as e:  # keep going
            print("   skipped: %s" % e, file=sys.stderr)
            continue
        c = Counter(x.status for x in f)
        rows.append((repo, len(f), c[cli.YES], c[cli.WONTFIX], c[cli.NO]))
        all_json[repo] = [x.to_dict() for x in f]

    rows.sort(key=lambda r: -r[2])
    total = sum(r[1] for r in rows)
    dead = sum(r[2] for r in rows)
    out = [
        "# Dead workarounds in %d popular repos" % len(rows), "",
        "canidelete found **%d GitHub issue links and tripwires in code comments**. **%d of them (%.0f%%) point at something "
        "that's already resolved**: the issue is closed, the PR merged, or the deadline passed. Not every one is dead code, "
        "but every one is a comment worth a second look." % (total, dead, 100.0 * dead / max(total, 1)), "",
        "| Repo | Links | ✅ Resolved | 🪦 Won't fix | ⏳ Still needed |", "|---|---:|---:|---:|---:|",
    ]
    out += ["| [%s](https://github.com/%s) | %d | **%d** | %d | %d |" % (r[0], r[0], r[1], r[2], r[3], r[4]) for r in rows]
    oldest = []
    for repo, fs in all_json.items():
        for f in fs:
            if f["status"] == cli.YES:
                for c in f["conditions"]:
                    if "closed" in c["detail"] and "y " in c["detail"]:
                        oldest.append((repo, f["file"], f["line"], c["text"], c["detail"]))
    if oldest:
        out += ["", "## Hall of fame: fixed years ago, still worked around", ""]
        for repo, file, line, text, detail in oldest[:25]:
            out.append("- `%s` [%s:%d](https://github.com/%s/blob/HEAD/%s#L%d) waits on %s, which was %s" % (
                repo, file, line, repo, file, line, text, detail))
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(all_json, fh, indent=1)
    print("\n".join(out[:4]))
    print("\nWrote study/RESULTS.md")


if __name__ == "__main__":
    main()
