#!/usr/bin/env python3
"""Install AI Berkshire skills (github.com/xbtlin/ai-berkshire, MIT) as Claude Code project skills.

Usage:
    python3 scripts/sync_ai_berkshire.py                 # clone upstream main and sync
    python3 scripts/sync_ai_berkshire.py --src PATH      # sync from an existing checkout
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "https://github.com/xbtlin/ai-berkshire"
SKILLS_DEST = ROOT / ".claude" / "skills"
TOOLS_DEST = ROOT / "tools"
LICENSE_DEST = ROOT / "licenses" / "ai-berkshire-LICENSE"

# Upstream writes reports to the home directory, which a cloud container discards.
REPORT_PATH = (re.compile(r"写入 `~/"), "写入 `reports/")
# investment-team only checks settings.local.json for the WebSearch grant; this repo grants it in settings.json.
SETTINGS_GREP = (
    ".claude/settings.local.json ~/.claude/settings.local.json",
    ".claude/settings.json .claude/settings.local.json ~/.claude/settings.json ~/.claude/settings.local.json",
)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :].lstrip("\n")


def first_heading(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def to_skill(name: str, text: str) -> str:
    meta, body = split_frontmatter(text)
    meta = meta or ""
    lines = []
    if not re.search(r"(?m)^name:\s*", meta):
        lines.append(f"name: {name}")
    if not re.search(r"(?m)^description:\s*", meta):
        title = first_heading(body, name)
        lines.append("description: " + yaml_quote(f"AI Berkshire(AI 버크셔) skill: {title}"))
    if meta.strip():
        lines.append(meta.rstrip())
    body = REPORT_PATH[0].sub(REPORT_PATH[1], body)
    body = body.replace(*SETTINGS_GREP)
    return "---\n" + "\n".join(lines) + "\n---\n\n" + body


def sync(src: Path) -> None:
    sources = sorted((src / "skills").glob("*.md"))
    if not sources:
        sys.exit(f"no skills/*.md under {src}")

    tools = set()
    for path in sources:
        name = path.stem
        text = path.read_text(encoding="utf-8")
        tools.update(re.findall(r"tools/([\w.-]+\.py)", text))
        dest = SKILLS_DEST / name
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        (dest / "SKILL.md").write_text(to_skill(name, text), encoding="utf-8")

    TOOLS_DEST.mkdir(exist_ok=True)
    for tool in sorted(tools):
        if (src / "tools" / tool).exists():
            shutil.copy2(src / "tools" / tool, TOOLS_DEST / tool)

    LICENSE_DEST.parent.mkdir(exist_ok=True)
    shutil.copy2(src / "LICENSE", LICENSE_DEST)

    rev = subprocess.run(
        ["git", "-C", str(src), "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    print(f"synced {len(sources)} skills, {len(tools)} tools from {UPSTREAM}@{rev or 'unknown'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--src", type=Path, help="existing ai-berkshire checkout")
    args = parser.parse_args()
    if args.src:
        sync(args.src)
        return
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"}
        subprocess.run(["git", "clone", "--depth", "1", UPSTREAM, tmp], check=True, env=env)
        sync(Path(tmp))


if __name__ == "__main__":
    main()
