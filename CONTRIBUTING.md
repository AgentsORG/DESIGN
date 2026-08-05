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
5. Update docs/ (especially diagrams)
6. Open a PR
```

## Regenerating examples

Requires temporary DESIGN.md downloads (gitignored):

```bash
# download sources into .tmp-*-DESIGN.md (see scripts/convert_getdesign.py)
python scripts/convert_getdesign.py
```

## Docs

- Hub: [docs/INDEX.md](docs/INDEX.md)
- Ecosystem: [docs/ecosystem.md](docs/ecosystem.md)
- Prefer Mermaid diagrams for architecture / flows

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

By contributing, you agree your contributions are licensed under the [MIT License](LICENSE).
