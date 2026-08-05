# UPDATE — edit `.design` in place

The file is the source of truth. Git is the audit trail.

## Modes

| Mode | When | Behavior |
| --- | --- | --- |
| `bootstrap` / `extract` | New or empty system from sources | Fill draft fields; `status: bootstrap`; populate `sources` |
| `update` | User asked to change brand/components | Edit unlocked fields; bump `version` + `updated_at` |
| `lock` / `unlock` | Release / exploration | Adjust `status` and `locked[]` with user intent |
| `verify` | Drift check | Report; edit only when asked to fix |

## Locked paths

```
Need to change a path?
├── Listed in locked[]?
│   ├── Yes → ASK the user first
│   └── No → edit, then SemVer bump if meaningful
```

## SemVer cheat sheet

| Change | Bump |
| --- | --- |
| Rename/remove token or variant consumers rely on | MAJOR (confirm with user) |
| Add token, variant, pattern, constraint | MINOR |
| Fix typo, clarify when_not, non-visual | PATCH |

## Sync from external tools

Claude Design, Stitch, Figma MCP, screenshots:

1. Record `sources`
2. Diff against current file
3. Merge unlocked changes
4. Ask before overwriting locked keys

## Do not

- Do not invent `ops.proposed_changes` or `history` arrays
- Do not silently delete locked keys
- Do not thrash version numbers on no-op edits
