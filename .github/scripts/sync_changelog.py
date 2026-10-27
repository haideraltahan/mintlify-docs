"""Turn oellm-eval's CHANGELOG.md (stdin) into the changelog.mdx page (stdout)."""

import re
import sys

REPO = "https://github.com/OpenEuroLLM/oellm-eval/blob/main/"

FRONTMATTER = """---
title: "Changelog"
description: "What changed in each oellm-eval release."
icon: "clock-rotate-left"
---

This page is copied every hour from [`CHANGELOG.md`]({repo}CHANGELOG.md) in the oellm-eval repository.
"""


def escape_mdx(line: str) -> str:
    """Escape the characters MDX parses as JSX, except inside inline code."""
    parts = line.split("`")
    parts[::2] = [
        p.replace("{", "\\{").replace("}", "\\}").replace("<", "&lt;")
        for p in parts[::2]
    ]
    return "`".join(parts)


def convert(text: str) -> str:
    text = re.sub(r"<!--.*?-->\n{0,2}", "", text, flags=re.S)  # MDX rejects HTML comments
    text = text.split("\n", 1)[1]  # the page title replaces "# Changelog"
    text = re.sub(r"\]\((?!https?://|#)", "](" + REPO, text)  # repo-relative links
    text = re.sub(r"^## \[(.+?)\]", r"## \1", text, flags=re.M)
    # Drop headings with nothing under them, e.g. the [Unreleased] template.
    text = re.sub(r"^### .*\n\s*(?=^##|\Z)", "", text, flags=re.M)
    text = re.sub(r"^## .*\n\s*(?=^## |\Z)", "", text, flags=re.M)

    lines, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        lines.append(line if in_fence else escape_mdx(line))
    return FRONTMATTER.format(repo=REPO) + "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    sys.stdout.write(convert(sys.stdin.read()))
