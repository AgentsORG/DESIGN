# Contributing

Thanks for helping make `.design` the living visual contract for AI design.

## Ground rules

1. **SPEC.md is normative.** Schema, skill, examples, and docs must follow it.
2. **No in-file history / proposal queues.** Git is the audit trail.
3. **DESIGN.md parity.** Do not drop component properties or rationale sections on import/export.
4. **Examples disclaimer.** Brand examples from getdesign.md are independent analyses — not affiliated with those companies.
5. **Keep PRs focused.** Spec change, schema, skill, examples, or docs — prefer separate commits when mixing.

## Development loop

```text
1. Edit SPEC.md (if format changes)
2. Sync schema/design.v1.schema.json
3. Update skills/design/ references
4. Refresh examples if needed:
     python scripts/convert_getdesign.py
5. Validate everything:
     python scripts/lint_design.py
6. Update docs/ (especially diagrams)
7. Open a PR — CI runs the same validation plus a leak guard
```

## Reference tooling

| Script | Purpose |
| --- | --- |
| `scripts/lint_design.py` | Schema + SPEC §19 lint over all examples/templates (runs in CI) |
| `scripts/export_design.py` | Emit `exports.*` artifacts: CSS variables (mode strategies), Tailwind v4 `@theme`, DTCG JSON, shadcn registry item |
| `scripts/diff_design.py` | SPEC §18 diff: added/removed/modified per token group + regression flag (`--fail-on-regression`) |
| `scripts/convert_getdesign.py` | Regenerate brand examples from DESIGN.md analyses |

```bash
pip install pyyaml jsonschema
python scripts/lint_design.py
python scripts/export_design.py templates/starter.design --out-dir /tmp/exports
python scripts/diff_design.py old.design new.design --fail-on-regression
```

## Regenerating examples

Requires temporary DESIGN.md downloads (gitignored):

```bash
# download sources into .tmp-*-DESIGN.md (see scripts/convert_getdesign.py BRANDS)
python scripts/convert_getdesign.py
python scripts/lint_design.py
```

## Docs

- Hub: [docs/INDEX.md](docs/INDEX.md)
- Ecosystem: [docs/ecosystem.md](docs/ecosystem.md)
- Prefer Mermaid diagrams for architecture / flows

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

By contributing, you agree your contributions are licensed under the [MIT License](LICENSE).
