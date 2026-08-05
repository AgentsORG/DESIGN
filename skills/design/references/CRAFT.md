# CRAFT — design-engineering bar

Apply these rules when generating or reviewing UI **whenever `.design` is silent**. Project `.design` tokens, constraints, rationale, and components always win on conflict.

Inspiration and attribution: [ATTRIBUTION.md](ATTRIBUTION.md).

**Styling systems:** detect and match the project’s existing approach (Tailwind, CSS, CSS Modules, CSS-in-JS, …). Never impose a new stack. Translate values into that system.

## Core principles

1. **One primary action per view.** Demote extras to secondary / ghost / text link.
2. **Hierarchy is subtraction.** Make the important thing prominent by making everything else recede.
3. **Restraint reads as intent.** Fewer colors, fewer font weights, one icon set.
4. **Specific beats generic.** “Save changes” beats “Submit”; empty states say why and what next.
5. **Borders and shadows recede.** Prefer alpha borders and layered shadows over solid pasted chrome.
6. **Semantic tokens over raw hex.** Use `{tokens.*}` / CSS vars; derive hovers with `color-mix` when possible.
7. **Space with system.** Parent `gap` over per-child margins; snap to `tokens.spacing`; line length ~65ch.
8. **Every state is designed.** Default, hover, focus, active, disabled, loading, empty, error.
9. **Accessibility is a floor.** Focus visible, labels, real buttons, 44×44 tap targets, `prefers-reduced-motion`.
10. **Nested radius is computed.** `innerRadius = outerRadius − padding` (when gap < ~24px).

## Typography

- Cap body measure at ~**65ch**.
- Paragraph spacing ≈ **1× line-height**, not an arbitrary px.
- Uppercase labels: **loosen tracking**.
- Tabular numbers (`font-variant-numeric: tabular-nums`) for prices / live data columns.
- Kill orphans: `text-wrap: balance` / `pretty` on headings (judge when a manual break is better).
- Declare fallback stacks that match x-height; load only weights you use.
- Never underline non-links; use `…` not `...`.
- Light weights are size-dependent — don’t use ultra-light at small sizes.
- Prefer optical kerning on large display type when available.

## Color & surfaces

- Light borders: soft alpha (e.g. `rgba(0,0,0,0.08)`); dark borders: quiet solids or low white alpha — don’t paste light-mode chrome into dark.
- Dark mode is **not** inverted light mode; preserve layering (top canvas stays the lightest dark surface).
- Desaturate brand accents ~20–30% on dark if they vibrate.
- Neutrals agree with brand hue; avoid pure `#808080`.
- If green is brand primary, don’t also use green for success — pick a distinct confirmation color.
- Disabled: dedicated muted token, not only `opacity: 0.4`.
- Elevation: layered translucent shadows in light; often a 1px ring in dark (`tokens.elevation`).
- Image outlines: low-opacity black (light) / white (dark), not tinted neutrals.
- Prefer `mask-image` for content fades; never fade scrollable reading content.

## Layout & spacing

- Prefer `gap` on parents; avoid trailing margin after last child.
- Cap wide marketing/content containers (~1200–1440px unless `.design` says otherwise).
- Breakpoints follow **content** failure points (`tokens.breakpoint`), not only device folklore.
- Sticky / fixed mobile CTAs honor `env(safe-area-inset-bottom)`.
- Text over full-bleed imagery needs a scrim + contrast check — or place text beside/below.

## Interaction & forms

- Hover confirms affordance (`@media (hover: hover) and (pointer: fine)`); never hover-only for core actions.
- Never bare `outline: none` — replace with visible focus ring + offset.
- Pressed state on buttons (slight scale/depress).
- Skeletons for long lists; spinner only when shape is unknown.
- Debounce search ~300ms; show clipboard success feedback ~1.5s.
- Labels associated with inputs; validation **inline** at the field.
- Inputs on mobile: font-size ≥ **16px** (avoid iOS zoom).
- Destructive actions separated from Confirm (space + visual break).

## Motion

Use `tokens.motion` when present; otherwise defaults:

| Kind | Duration | Notes |
| --- | --- | --- |
| Hover / color | 100–150ms | Soft ease |
| Tooltip / dropdown | 150–250ms | `ease-out` enter |
| Modal / drawer | 200–300ms | Under 300ms for product UI |
| Page transition | ≤ 400ms | Marketing may go longer |

Rules:

- Animate **`transform` / `opacity` only** — never width/height/margin/top/left.
- Never `transition: all`.
- Enter `ease-out` (prefer `cubic-bezier(0.32, 0.72, 0, 1)`); avoid `ease-in` on enters.
- Exits ~20–30% faster than enters; don’t animate 100+/day or keyboard-driven actions.
- Don’t enter from `scale(0)` — start ~`0.95` + opacity 0.
- Origin-aware popovers (scale from trigger).
- Honor **`prefers-reduced-motion`**; disable theme-switch cascades when possible.
- Stagger list entrances (~40ms) when many items would flash.

## Marketing / hero restraint

When `.design` `patterns` or rationale don’t specify:

- First viewport: brand, one headline, one supporting line, one CTA group, one dominant visual — no card soup, stat strips, or floating promo chips in the hero.
- Match project brand; avoid generic purple-on-white AI chrome unless the contract says so.

## Component APIs (when inventing)

- Composition over configuration; prefer catalog / shadcn primitives.
- After inventing an approved control, **UPDATE** `.design` `components` so the next session doesn’t fork it.
- Avoid boolean-prop explosion; support controlled + uncontrolled when state is involved.

## Copy

- Sentence case for UI; outcome-specific button labels.
- Errors tell how to fix; placeholders are not labels.
- Empty states: context + next action.
- Drop filler “please” from short imperatives.

## When `.design` speaks

```
CRAFT rule conflicts with tokens / constraints / rationale / when_when_not?
└── .design wins — follow the contract, note the override briefly
```
