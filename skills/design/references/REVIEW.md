# REVIEW — compliance after UI generate or on verify

Review like a design engineer with a low tolerance for “it works.” AI UI often passes the happy path and fails details.

## Verdict

Lead with one line: **Blocked** | **Approve with changes** | **Ship it**.

- **Blocked** — interaction broken, a11y floor failed, or `constraints.never` violated  
- **Approve with changes** — craft issues; must-fix before merge preferred  
- **Ship it** — no findings against `.design` and a11y floor  

## Priority order

1. **Interaction correctness** — controls work with pointer, keyboard, touch  
2. **Accessibility floor** — focus visible, labels, contrast per `policy.accessibility`, `prefers-reduced-motion` honored  
3. **Token compliance** — no hardcoded colors/spacing/radius when tokens exist  
4. **shadcn sync** — if `integrations.shadcn.enabled`, `globals.css` matches `css_vars` / tokens; `cssVariables: true` in components.json  
5. **Component compliance** — catalog components used; `when`/`when_not` respected; one primary CTA if constrained  
6. **Pattern compliance** — forbidden pattern parts absent  
7. **Hierarchy / spacing** — consistent scale; primary action clear  
8. **Motion** — within `tokens.motion` budgets if defined  

## Escalation triggers (flag on sight)

- Raw hex/rgb/hsl in UI source when `tokens.color` defines semantics  
- Second filled primary button on the same view when constrained  
- Off-system font families  
- Items listed in `constraints.never` (gradients, glassmorphism, etc.)  
- Invented component that duplicates a catalog entry  
- Missing focus ring / `outline: none` without replacement  
- Animating layout properties when transform/opacity would do  
- Icon-only control without accessible name  
- shadcn enabled but theme still on default zinc/neutral while `.design` defines a brand palette  

## Verify against code

| Check | Pass criteria |
| --- | --- |
| `token-lint` | CSS vars / Tailwind theme include semantic tokens from `.design` |
| `shadcn-css` | `:root` / `.dark` in `integrations.shadcn.css` match `css_vars` (tokens win on conflict) |
| `components-json` | `style`, aliases, `cssVariables` align with `integrations.shadcn` |
| `component-grep` | `components.*.import` paths exist; variants appear in code or docs |
| `hardcode-scan` | No unexplained raw palette values in touched UI files |
| `contrast` | Component fg/bg pairs meet `policy.accessibility.contrast` when checkable |

On fail: report findings. Update `.design` only when the user asks to reconcile.

## Finding format

For each issue: what is wrong, where (`file:line` if possible), why it violates `.design` or a11y, and the fix (token/component to use).
