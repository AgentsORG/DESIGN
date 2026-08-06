#!/usr/bin/env python3
"""Validate all .design files against the schema and core SPEC §19 lint rules.

Usage: python scripts/lint_design.py
Exit code 0 = all files pass (warnings allowed), 1 = any error.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]

REF_RE = re.compile(r"\{(tokens\.[A-Za-z0-9_.\-]+)\}")
MAX_REF_DEPTH = 10
MAX_NEST_DEPTH = 20


def resolve_path(doc: dict, dotted: str):
    node = doc
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def token_refs_in(value) -> list[str]:
    if isinstance(value, str):
        return REF_RE.findall(value)
    if isinstance(value, dict):
        return [r for v in value.values() for r in token_refs_in(v)]
    if isinstance(value, list):
        return [r for v in value for r in token_refs_in(v)]
    return []


def nesting_depth(node, depth=0) -> int:
    if not isinstance(node, dict):
        return depth
    return max((nesting_depth(v, depth + 1) for v in node.values()), default=depth)


def lint(path: pathlib.Path, validator: Draft202012Validator) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))

    for err in validator.iter_errors(doc):
        errors.append(f"schema: {'/'.join(map(str, err.absolute_path))}: {err.message[:140]}")

    agent = doc.get("agent") or {}
    if not (agent.get("instructions") or "").strip():
        errors.append("missing agent.instructions (file must be self-contained)")

    intent = doc.get("intent")
    if isinstance(intent, dict) and not (intent.get("reference") or "").strip():
        errors.append("intent present without intent.reference")

    components = doc.get("components") or {}
    for cid, comp in components.items():
        if isinstance(comp, dict) and comp.get("variants"):
            if not (comp.get("when") or comp.get("when_not")):
                errors.append(f"components.{cid}: variants without when/when_not")

    tokens = doc.get("tokens") or {}
    if nesting_depth(tokens) > MAX_NEST_DEPTH + 1:
        errors.append(f"tokens nesting exceeds depth {MAX_NEST_DEPTH}")

    omitted = {
        (o.get("section") if isinstance(o, dict) else o)
        for o in (doc.get("omitted") or [])
    }
    color = tokens.get("color") or {}
    if "primary" not in color and "tokens.color.primary" not in omitted and "colors" not in omitted:
        warnings.append("no tokens.color.primary (add or declare in omitted)")
    if not tokens.get("typography") and "tokens.typography" not in omitted and "typography" not in omitted:
        warnings.append("no tokens.typography (add or declare in omitted)")

    # broken / deep token references (search normative fields)
    for section in ("tokens", "components", "themes", "integrations"):
        for ref in set(token_refs_in(doc.get(section))):
            seen: list[str] = []
            current = ref
            for _ in range(MAX_REF_DEPTH + 1):
                target = resolve_path(doc, current)
                if target is None:
                    errors.append(f"{section}: broken reference {{{ref}}}")
                    break
                if isinstance(target, str) and REF_RE.fullmatch(target.strip()):
                    nxt = target.strip()[1:-1]
                    if nxt in seen:
                        errors.append(f"{section}: circular reference {{{ref}}}")
                        break
                    seen.append(nxt)
                    current = nxt
                    continue
                break
            else:
                errors.append(f"{section}: reference chain deeper than {MAX_REF_DEPTH} at {{{ref}}}")

    return errors, warnings


def main() -> int:
    schema = json.loads((ROOT / "schema" / "design.v1.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    files = sorted(ROOT.glob("examples/*.design")) + sorted(
        ROOT.glob("skills/design/examples/*.design")
    )
    if not files:
        print("no .design files found")
        return 1

    failed = False
    for path in files:
        rel = path.relative_to(ROOT)
        errors, warnings = lint(path, validator)
        for w in warnings:
            print(f"WARN  {rel}: {w}")
        for e in errors:
            print(f"ERROR {rel}: {e}")
        if errors:
            failed = True
        else:
            print(f"OK    {rel}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
