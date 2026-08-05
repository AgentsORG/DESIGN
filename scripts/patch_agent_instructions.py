#!/usr/bin/env python3
"""Patch agent.instructions in all examples/*.design to the self-contained template."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from convert_getdesign import SELF_CONTAINED_INSTRUCTIONS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def patch_file(path: pathlib.Path) -> bool:
    text = path.read_text(encoding="utf-8")
    block = "agent:\n  skill: design\n  instructions: |\n"
    for line in SELF_CONTAINED_INSTRUCTIONS.splitlines():
        block += f"    {line}\n" if line else "    \n"
    # Replace existing agent: … through blank line before next top-level key
    new, n = re.subn(
        r"^agent:\n(?:  .*\n)+",
        block + "\n",
        text,
        count=1,
        flags=re.M,
    )
    if n == 0:
        print("no agent block", path.name)
        return False
    path.write_text(new, encoding="utf-8")
    print("patched", path.name)
    return True


def main():
    for p in sorted(EXAMPLES.glob("*.design")):
        patch_file(p)
    minimal = ROOT / "skills" / "design" / "examples" / "minimal.design"
    if minimal.exists():
        patch_file(minimal)


if __name__ == "__main__":
    main()
