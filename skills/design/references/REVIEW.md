# REVIEW — compliance after UI generate or on verify

Review like a design engineer with a low tolerance for “it works.” AI UI often passes the happy path and fails details. Approval is earned, not assumed.

Cross-check craft defaults in [CRAFT.md](CRAFT.md). Project `.design` still wins on conflict.

## Verdict

Lead with one line: **Blocked** | **Approve with changes** | **Ship it**.

- **Blocked** — interaction broken, a11y floor failed, or `constraints.never` violated  
- **Approve with changes** — craft issues; must-fix before merge preferred  
- **Ship it** — no findings against `.design`, CRAFT floor, and a11y  

Then list **Blocking**, **Should fix**, and **Nits** (optional). Don’t bury one blocker under ten nits. A clean **Ship it** is a real outcome — never manufacture nitpicks to look thorough.

## Priority order (triage)

1. **Interaction correctness** — mouse, keyboard, touch; Enter/Escape; no hover-only core actions  
2. **Accessibility floor** — 44×44 targets, labeled icon buttons, focus visible, contrast, `prefers-reduced-motion`  
3. **Layout stability** — tabular nums / reserved space for dynamic values; no weight change on hover  
4. **Token / `.design` compliance** — no hardcoded colors/spacing/radius when tokens exist; bind component property bags  
5. **shadcn sync** — if enabled, `globals.css` ↔ `css_vars` / tokens; `cssVariables: true`  
6. **Component / pattern compliance** — catalog + `when`/`when_not`; one primary CTA if constrained  
7. **Motion** — justified, <300ms product UI, transform/opacity only, matches `tokens.motion`  
8. **Spacing & hierarchy** — scale, alignment, restraint ([CRAFT.md](CRAFT.md))  
9. **Type & surfaces** — measure ~65ch, nested radii, coherent borders/shadows  
10. **Final polish** — empty/loading/selection states  

## Escalation triggers (flag on sight)

**Contract / brand**

- Raw hex/rgb/hsl when `tokens.color` defines semantics  
- Second filled primary on the same view when constrained  
- Off-system fonts; `constraints.never` items  
- Invented duplicate of a catalog component  
- shadcn enabled but still default zinc/neutral while `.design` has a brand palette  
- Dropped DESIGN.md component properties or rationale during restyle  

**Craft / a11y / motion**

- `transition: all` — including a bare utility `transition` class (it compiles to `transition-property: all`)  
- Hover-only access to a core action  
- Icon-only control with no accessible name  
- Animating `width` / `height` / `margin` / `top` / `left` instead of `transform` / `opacity`  
- `ease-in` on UI enters; animation on keyboard / 100+/day actions  
- Dynamic number without reserved space or `tabular-nums`  
- `<input>` font-size under 16px (iOS zoom)  
- Random `z-index: 9999` instead of a scale (`tokens.zIndex`)  
- Font weight change on hover/active (layout shift)  
- Missing `prefers-reduced-motion` on motion (reduced = gentler, not zero: keep brief opacity/color feedback)  
- Bare `outline: none` without a replacement focus ring  
- Nested child reusing parent radius (pinched corners)  
- Unbounded list rendered without virtualization (~50+ items possible)  
- Raster image scaled above its natural size  
- Focus not returned to the trigger after an overlay closes  
- Blanket `will-change` (or `will-change` on non-compositor properties)  
- `position: sticky` silently dead under an ancestor's `overflow: hidden`  

**Exemption:** centered modals/dialogs correctly use `transform-origin: center` — origin-aware scaling applies to trigger-anchored surfaces (popovers, dropdowns, tooltips) only. Do not flag it.

## Findings table (required for craft issues)

Present craft findings as a markdown table:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` on Button | `transition: transform 150ms, opacity 150ms` | Unbounded `all` animates layout props |

Be specific (cite values, `file:line` when possible). For `.design` violations, name the token/component path to use.

## Fixing motion (remedial order)

When a motion finding needs a fix, prefer remedies in this order — deleting is often the strongest fix:

1. Delete the animation
2. Reduce it (shorter, smaller, fewer properties)
3. Fix easing
4. Fix origin / physicality
5. Make it interruptible (transition/spring instead of keyframes)
6. Move it to `transform` / `opacity`
7. Make timing asymmetric (fast response, slow deliberation)
8. Polish (blur bridge, stagger)

When feel cannot be judged from code, run the animation at 2–5× duration (or step frame-by-frame in the browser's animation inspector); test gestures on a real device; re-judge with fresh eyes before sign-off — timing desyncs between coordinated properties are invisible at full speed.

## Verify against code

| Check | Pass criteria |
| --- | --- |
| `token-lint` | CSS vars / Tailwind theme include semantic tokens from `.design` |
| `shadcn-css` | `:root` / `.dark` match `css_vars` (tokens win on conflict) |
| `components-json` | `style`, aliases, `cssVariables` align with `integrations.shadcn` |
| `component-grep` | import paths / variants exist |
| `hardcode-scan` | No unexplained raw palette values in touched UI |
| `contrast` | fg/bg meet `policy.accessibility.contrast` when checkable |
| `craft-scan` | No escalation triggers above; CRAFT defaults where contract is silent |

On fail: report findings. Update `.design` only when the user asks to reconcile.
