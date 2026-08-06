# Examples

Brand-inspired `.design` contracts for teaching and bootstrap.

> **Not affiliated** with the named companies. See [NOTICE.md](../NOTICE.md).

| File | Source analysis |
| --- | --- |
| [vercel.design](vercel.design) | [getdesign.md/vercel](https://getdesign.md/vercel/design-md) |
| [stripe.design](stripe.design) | [getdesign.md/stripe](https://getdesign.md/stripe/design-md) |
| [notion.design](notion.design) | [getdesign.md/notion](https://getdesign.md/notion/design-md) |
| [apple.design](apple.design) | [getdesign.md/apple](https://getdesign.md/apple/design-md) |
| [linear.design](linear.design) | [getdesign.md/linear.app](https://getdesign.md/linear.app/design-md) |
| [supabase.design](supabase.design) | [getdesign.md/supabase](https://getdesign.md/supabase/design-md) |

Each file includes:

- Full `tokens.*` from DESIGN.md frontmatter  
- `intent` with `direction` (committed aesthetic) and `signature` (the one bold element)  
- `voice` — the UI copy contract (register, casing, terminology)  
- All component property bags (`backgroundColor`, `textColor`, …)  
- `rationale.*` from DESIGN.md body sections  
- `integrations.shadcn` theme mapping  
- Self-contained `agent.instructions`  

CI validates every example against the design.v1 schema and lint rules (`scripts/lint_design.py`).

```bash
cp examples/stripe.design ./.design
# then adapt name / intent / locked for your product
```

Regenerate:

```bash
python scripts/convert_getdesign.py
```
