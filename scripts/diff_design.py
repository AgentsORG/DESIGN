#!/usr/bin/env python3
"""Diff two .design files per SPEC §18: added / removed / modified per token
group, component variant changes, and a regression flag.

A regression is anything consumers may rely on that was removed or changed:
removed/modified tokens, removed components or variants, removed locked paths.

Usage:
  python scripts/diff_design.py <old.design> <new.design> [--fail-on-regression]

Exit code: 0 (no regression, or informational), 2 with --fail-on-regression
when a regression is detected.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import yaml


def flatten(node, path=()):
    if isinstance(node, dict):
        for key, val in node.items():
            yield from flatten(val, path + (str(key),))
    else:
        yield ".".join(path), node


def token_map(doc: dict) -> dict[str, object]:
    return dict(flatten(doc.get("tokens") or {}))


def component_variants(doc: dict) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for cid, comp in (doc.get("components") or {}).items():
        if not isinstance(comp, dict):
            continue
        variants = set(comp.get("variants") or [])
        variants |= set((comp.get("tokens") or {}).keys())
        out[cid] = variants
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", type=pathlib.Path)
    parser.add_argument("new", type=pathlib.Path)
    parser.add_argument("--fail-on-regression", action="store_true")
    args = parser.parse_args()

    old = yaml.safe_load(args.old.read_text(encoding="utf-8"))
    new = yaml.safe_load(args.new.read_text(encoding="utf-8"))

    old_tokens, new_tokens = token_map(old), token_map(new)
    added = sorted(set(new_tokens) - set(old_tokens))
    removed = sorted(set(old_tokens) - set(new_tokens))
    modified = sorted(
        k for k in set(old_tokens) & set(new_tokens) if old_tokens[k] != new_tokens[k]
    )

    by_group: dict[str, dict[str, list[str]]] = {}
    for kind, keys in (("added", added), ("removed", removed), ("modified", modified)):
        for key in keys:
            group = key.split(".", 1)[0]
            by_group.setdefault(group, {}).setdefault(kind, []).append(key)

    old_comp, new_comp = component_variants(old), component_variants(new)
    comp_removed = sorted(set(old_comp) - set(new_comp))
    comp_added = sorted(set(new_comp) - set(old_comp))
    variant_removed = {
        cid: sorted(old_comp[cid] - new_comp[cid])
        for cid in set(old_comp) & set(new_comp)
        if old_comp[cid] - new_comp[cid]
    }

    locked_removed = sorted(set(old.get("locked") or []) - set(new.get("locked") or []))

    regression = bool(removed or modified or comp_removed or variant_removed or locked_removed)

    print(f"diff {args.old.name} -> {args.new.name}")
    if not by_group and not comp_added and not comp_removed and not variant_removed:
        print("  tokens: no changes")
    for group, kinds in sorted(by_group.items()):
        summary = ", ".join(f"{k} {len(v)}" for k, v in kinds.items())
        print(f"  tokens.{group}: {summary}")
        for kind, keys in kinds.items():
            for key in keys[:10]:
                marker = {"added": "+", "removed": "-", "modified": "~"}[kind]
                print(f"    {marker} {key}")
            if len(keys) > 10:
                print(f"    … {len(keys) - 10} more")
    for cid in comp_added:
        print(f"  components: + {cid}")
    for cid in comp_removed:
        print(f"  components: - {cid}")
    for cid, variants in variant_removed.items():
        print(f"  components.{cid}: removed variants {', '.join(variants)}")
    for path in locked_removed:
        print(f"  locked: - {path}")

    old_v, new_v = old.get("version"), new.get("version")
    if old_v != new_v:
        print(f"  version: {old_v} -> {new_v}")
    print(f"  regression: {'YES' if regression else 'no'}")
    if regression and old_v == new_v:
        print("  note: regression without a version bump — SPEC §18 expects MAJOR/MINOR SemVer movement")

    return 2 if (regression and args.fail_on_regression) else 0


if __name__ == "__main__":
    sys.exit(main())
