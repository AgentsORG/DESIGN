#!/usr/bin/env python3
"""Patch agent.instructions in all .design files to the canonical template.

The template lives in convert_getdesign.SELF_CONTAINED_INSTRUCTIONS (single
source of truth). Brand-analysis examples get the DISCLAIMER suffix; generic
files (templates/, skills/design/examples/) do not. Idempotent: files already
carrying the current template are left untouched.
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from convert_getdesign import BRAND_DISCLAIMER, SELF_CONTAINED_INSTRUCTIONS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]

# agent: mapping through its indented block, including interior blank lines,
# up to (not including) the next top-level key or end of file
AGENT_BLOCK_RE = re.compile(r"^agent:\n(?:(?:[ \t]+.*)?\n)*?(?=\S|\Z)", re.M)


def build_block(with_disclaimer: bool) -> str:
    body = SELF_CONTAINED_INSTRUCTIONS + (BRAND_DISCLAIMER if with_disclaimer else "")
    block = "agent:\n  skill: design\n  instructions: |\n"
    for line in body.splitlines():
        block += f"    {line}\n" if line else "    \n"
    return block + "\n"


def patch_file(path: pathlib.Path, with_disclaimer: bool) -> None:
    text = path.read_text(encoding="utf-8")
    block = build_block(with_disclaimer)
    new, n = AGENT_BLOCK_RE.subn(block, text, count=1)
    if n == 0:
        print("no agent block", path.name)
        return
    if new == text:
        print("unchanged", path.name)
        return
    path.write_text(new, encoding="utf-8", newline="\n")
    print("patched", path.name)


def main() -> int:
    for p in sorted((ROOT / "examples").glob("*.design")):
        patch_file(p, with_disclaimer=True)
    for p in sorted((ROOT / "templates").glob("*.design")):
        patch_file(p, with_disclaimer=False)
    minimal = ROOT / "skills" / "design" / "examples" / "minimal.design"
    if minimal.exists():
        patch_file(minimal, with_disclaimer=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
