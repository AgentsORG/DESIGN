# CRAFT — design-engineering bar

Apply these rules when generating or reviewing UI **whenever `.design` is silent**. Project `.design` tokens, constraints, rationale, and components always win on conflict.

**Styling systems:** detect and match the project’s existing approach (Tailwind, CSS, CSS Modules, CSS-in-JS, …). Never impose a new stack. Translate values into that system.

## Core principles

1. **One primary action per view.** Demote extras to secondary / ghost / text link.
2. **Hierarchy is subtraction.** Make the important thing prominent by making everything else recede.
3. **Restraint reads as intent.** Fewer colors, fewer font weights, one icon set — spend boldness in one signature element and keep everything around it quiet.
4. **Specific beats generic.** “Save changes” beats “Submit”; empty states say why and what next.
5. **Borders and shadows recede.** Prefer alpha borders and layered shadows over solid pasted chrome.
6. **Semantic tokens over raw hex.** Use `{tokens.*}` / CSS vars; derive hovers with `color-mix` when possible.
7. **Space with system.** Parent `gap` over per-child margins; snap to `tokens.spacing`; line length ~65ch.
8. **Every state is designed.** Default, hover, focus, active, disabled, loading, empty, error.
9. **Accessibility is a floor.** Focus visible, labels, real buttons, 44×44 tap targets, `prefers-reduced-motion`.
10. **Nested radius is computed.** `innerRadius = outerRadius − padding` (when gap < ~24px).
11. **Structure encodes meaning.** Numbering (01/02/03), eyebrows, and dividers signal true sequence or grouping — never decoration.
12. **First paint renders real state.** Persist interactive state and set it before render — never default-then-correct (the theme flash on refresh).

## Typography

- Cap body measure at ~**65ch**.
- Line-height is unitless, never px: ~**1.1** for display/headings, **1.5–1.6** for body.
- Tracking follows size: ~**−0.015em** on large display type, ~**+0.06em** on small uppercase labels, zero at body sizes — never one value for all.
- Paragraph spacing ≈ **1× line-height**, not an arbitrary px.
- Text size floors: **16px** body, **14px** dense UI controls, **13px** captions, almost never below 12px — and layouts must survive user zoom and enlarged root font size.
- Every font-size comes from a closed scale; name steps by role (`caption`, `body-lg`), not size, so the name polices its own usage.
- Pair typefaces across categories (serif display over sans text), never within them; two faces cover most products, three is the ceiling; match optical cuts to the size being set.
- Tabular numbers (`font-variant-numeric: tabular-nums`) for prices / live data columns.
- Kill orphans: `text-wrap: balance` / `pretty` on headings (judge when a manual break is better).
- Declare fallback stacks that match x-height; load only weights you use; serve **woff2 only**, subset to the characters actually used.
- Declare `font-synthesis: none` at the root so a missing bold/italic file fails visibly instead of being faked by the browser.
- Prefer high-level font properties (`font-weight`, `font-optical-sizing`, `font-variant-numeric`) over raw `font-variation-settings` / `font-feature-settings`; reserve raw tags for custom axes and numbered stylistic sets.
- Never change font weight on hover or selection — hold weight constant and signal state with color.
- Guard overflow per role: `overflow-wrap: break-word` wherever user-supplied tokens/URLs appear; `white-space: nowrap` on badges, buttons, and short labels.
- Truncation must leave a route to the full text (tooltip, `title`, expand, detail view) — a clipped ID with no escape hatch is data loss.
- Use real punctuation: `…` not `...`, en dash for ranges (Mon–Fri), em dash for asides, non-breaking space between value and unit (42 GB), soft hyphens in long words.
- Never underline non-links; tune real underlines with `text-decoration-thickness` / `underline-offset` / skip-ink; dotted underline is the settled “hover for more” cue; underline animation beyond a color fade needs its own element.
- Declare font smoothing (antialiased + grayscale) once at the layout root, never per component.
- Write direction-neutral CSS: logical properties (`margin-inline-start`, `text-align: start`) over physical ones; declare `lang` / `dir`.
- Size text-adjacent spacing in rem/em, not fixed px, so layout scales with the user’s text-size preference.
- Optically center labels by trimming the font’s built-in leading (`text-box: trim-both cap alphabetic`) as progressive enhancement.
- Light weights are size-dependent — don’t use ultra-light at small sizes.
- Prefer optical kerning on large display type when available.

## Color & surfaces

- Author and derive colors in **OKLCH**; keep hex only for third-party consumers that parse hex; leave keywords (`currentColor`, `transparent`) untouched.
- Contrast lives in the lightness gap: repair a failing pair by moving **L only**, keeping chroma and hue — raising saturation does nothing.
- Contrast floors are size-aware: **4.5:1** body text, **3:1** only for large text (~24px+, or bold ~18.5px+) and UI components — checked in both themes. APCA when used: |Lc| ≥ 60 body (75 preferred), ≥ 45 large/heavy, ≥ 30 non-text essentials; still satisfy WCAG ratios when compliance language names them.
- First-guess pairing: surfaces with L > 0.6 want dark text; near-white grounds (L ≥ 0.85) want foreground L ≤ 0.45; near-black grounds (L ≤ 0.25) want L ≥ 0.75 — then verify with a real check.
- A tonal ramp holds one hue; if an inherited scale drifts more than ~10° end to end, rebuild it on the mid-tone hue.
- Build ramps by anchoring endpoints near L 0.97 / 0.22, spacing L evenly, and shaping chroma as a curve (~30% of each step’s gamut ceiling at the ends, rising to ~85% mid-scale, clamped per step).
- Sibling hues (brand / success / warning) equalize by same L per step and the same *fraction* of each hue’s own chroma ceiling — never the same absolute chroma.
- Derive dark themes by remapping which scale steps the semantic roles point at (50↔950, 200↔800, 300↔700) — never by hand-picking a second palette.
- Dark mode is **not** inverted light mode; preserve layering (top canvas stays the lightest dark surface); desaturate brand accents ~20–30% on dark if they vibrate.
- Switch themes by flipping token values at the theme root; never scatter per-component dark-mode overrides.
- Check gamut before shipping high chroma: clamp C holding L and H when a value exceeds sRGB; serve wider-gamut chroma behind `@media (color-gamut: p3)` on an sRGB-safe base.
- Build light tints by reducing chroma, not by dropping opacity — opacity tints go grey and shift over non-white surfaces.
- Neutrals carry a slight hue bias toward the accent — a grey that was picked, not inherited; avoid pure `#808080`.
- If green is brand primary, don’t also use green for success — pick a distinct confirmation color.
- Disabled: dedicated muted token, not only `opacity: 0.4`.
- Shadows for **elevation** (cards, menus, popovers, anything raised); borders for **separation** (row dividers, gridlines, form-field edges) — a visible input border is an accessibility feature, never convert it to a shadow.
- Elevation recipe: 1px low-alpha spread ring + tight crisp shadow + wide soft ambient layer; on hover transition `box-shadow` only. In dark mode elevation is often a 1px ring (`tokens.elevation`).
- Light borders: soft alpha (e.g. `rgba(0,0,0,0.08)`); dark borders: quiet solids or low white alpha — don’t paste light-mode chrome into dark.
- Render hairline dividers at 0.5px on ≥2x displays via a media-query variable, falling back to 1px.
- Ease large gradients with multiple curve-following stops — a two-stop linear gradient between solids bands visibly.
- Image outlines: `outline` (not `border`) at 1px, `outline-offset: -1px`, pure black at 10% in light / pure white at 10% in dark — never tinted neutrals or accents.
- Translucent chrome discipline: never stack a light translucent surface on another; larger surfaces get stronger blur and deeper shadow than small chips; text over blur gets higher contrast and slightly heavier weight.
- Where content meets floating chrome, prefer a scroll-edge fade (small mask, only where overlap occurs) over a permanent 1px divider under sticky headers.
- Blocking modal tasks pair the surface with a dimming scrim; parallel non-blocking panels use elevation/translucency without one.
- Prefer `mask-image` for content fades; never fade scrollable reading content.
- Style `::selection` where the default clashes with the surface.

## Layout & spacing

- Prefer `gap` on parents; avoid trailing margin after last child.
- Cap wide marketing/content containers (~1200–1440px unless `.design` says otherwise).
- Breakpoints follow **content** failure points (`tokens.breakpoint`), not only device folklore.
- Reserve space for everything asynchronous: images declare dimensions or `aspect-ratio`, skeletons match the loaded state’s exact box, empty states are sized to the filled state.
- Wide content (tables, code, diagrams) scrolls inside its own `overflow-x: auto` container — the body never scrolls sideways.
- Contain stacking with `isolation: isolate` (or `position: relative`) so children can’t leak above unrelated UI; `z-index` only from the project scale.
- Cascade hygiene: scope section styles so one section’s selectors can’t cancel another’s; prefer single-purpose classes over escalating specificity.
- Use `dvh`, not `vh`, for mobile full-height layouts; cap sticky header heights with `max-height`.
- An ancestor with `overflow: hidden` silently disables `position: sticky` on descendants — check the chain when sticky “does nothing”.
- Give anchor targets `scroll-margin-top` equal to the sticky header height.
- Never restyle the page scrollbar; customize scrollbars only inside small scrollers (code blocks, panels) — ~8px wide, translucent rounded thumb.
- On long pages, keep the primary action persistently in view (sticky/anchored), not only at the bottom.
- Sticky / fixed mobile CTAs honor `env(safe-area-inset-bottom)`.
- Text over full-bleed imagery needs a scrim + contrast check — or place text beside/below.

## Iconography & illustration

- Icons are drawn per size, never scaled: thin the stroke at 16px vs 24px, switch to filled variants below ~12px, redraw heavier for large sizes, snap coordinates to whole pixels.
- Align by eye, not math: trailing-icon side padding = text-side padding − 2px; nudge directional glyphs (play triangles, arrows) 1–2px toward the pointed side; fix asymmetric SVGs in the viewBox.
- One icon, one meaning: don’t reuse a chevron for both expand and navigate; pairs differing only by rotation (upload/download) need a second distinguishing signal; ambiguous metaphors get a text label.
- Icons harmonize with text: stroke weight matches adjacent text weight, 6–8px gap between icon and label, round caps by default, each icon unioned to a single path with one fill.
- Favicons use a simplified mark pixel-hinted for 16px — a full logo at favicon size turns to mush.
- Illustrations obey the system: stroke weight matches the icon set, palette limited to ~3 token colors (recolor stock packs), light direction matches the UI’s shadows, complexity matches context (spot illustration in a tooltip, not a scene), redraw rather than scale.
- Code-built illustrations and decorative layers are labeled and inert: `role="img"` + `aria-label` (or `aria-hidden` when purely decorative), `pointer-events: none`, `user-select: none`.

## Interaction & forms

- Hover confirms affordance (`@media (hover: hover) and (pointer: fine)`); never hover-only for core actions.
- Hit areas ≥ **44×44px** touch, ≥ **40×40px** desktop: extend small controls with an absolutely-positioned pseudo-element (negative inset) — grow the hit area, never the visual — and shrink any extension that would overlap a neighbor.
- Commit actions on release (click / mouseup), not mousedown, so users can cancel by dragging away.
- Press feedback: scale **0.95–0.98** (default ~0.96) on `:active` via a ~150ms ease-out transition so a mid-press release glides back; never below 0.95; hover scale stays at 1–2%; skip press scale on dense or high-frequency controls.
- Never bare `outline: none` — style `:focus-visible` (not bare `:focus`) with a visible ring + offset; when no focus token exists, keep rings neutral (grey/black/white) and high-contrast, never a clashing accent.
- Any wait over **400ms** gets a visible indicator; pick by knowledge: skeleton when shape is known, determinate progress bar when duration is known, spinner only for short unknown waits.
- Prefer optimistic updates that roll back on error over blocking on the server.
- Debounce search ~300ms; clipboard success feedback ~1.5s; toast duration scales with content length (reading speed ~200–250 wpm), never a flat 2s.
- Sliders update their value live during drag, not on release.
- Overlay conduct: trap focus inside, make the background `inert`, move focus in on open, light dismiss (Escape + outside click), return focus to the trigger on close; arrow keys move within menus and lists; focus never lands off-screen.
- Hidden or off-screen content leaves the tab order: hide with `display: none`, `visibility: hidden`, or `inert` — never `opacity: 0` or off-screen transforms.
- Keep DOM order matching visual order; give pages with long navigation a visually hidden skip-to-content link that appears on focus.
- Disabled controls are actually inert — removed from tab order or explained — not merely greyed while still firing events.
- Submenus need a diagonal safe area (a triangular pointer-tracking zone between trigger and submenu) so diagonal cursor travel doesn’t close them mid-flight.
- Set `touch-action: manipulation` on buttons, links, and inputs (kills double-tap-zoom delay); `touch-action: none` on surfaces implementing their own pan/zoom/drag.
- Autoplaying video requires both `muted` and `playsinline`.
- Pause countdowns and time-limited actions while the tab is hidden; resume with remaining time.
- Use the semantically correct input type (`email`, `tel`, `url`, `number`, `search`, `password`) — right keyboard, native validation, autofill for free.
- Inputs on small viewports: font-size ≥ **16px**; never patch iOS zoom with `maximum-scale=1` (strips zoom elsewhere — a WCAG 1.4.4 failure).
- Labels associated with inputs; `aria-label` describes the action (“Search”), never the element (“icon”).
- Error states carry three signals — colored border, icon, message text — never color alone; validation renders **inline** at the field.
- Validate on blur or submit for a field’s first pass; once a field has errored, revalidate on every change so the error clears the moment it’s fixed.
- Wrap inputs in a real `<form>` so Enter submits; textareas submit on Cmd/Ctrl+Enter.
- Disable the submit control while a request is in flight and change its label to state progress.
- Autofocus the first input when a desktop modal containing one opens; never autofocus on touch devices.
- Input decorations (icons, prefixes, clear buttons) are absolutely positioned over the input with padding reserving room — never siblings; clickable decorations refocus the input.
- Checkbox and radio rows are clickable across their full extent — control, label, and the gap between.
- Keep autocomplete and spellcheck ON for identity, address, and payment fields; OFF for usernames, search, codes, and slugs.
- Prefill forms from known user data and link context — a “change username” link lands on a form already carrying the current value.
- Skeletons for long lists; spinner only when shape is unknown.
- Destructive actions: spatially separated from Confirm **and** behind an explicit confirmation (dialog or hold-to-confirm fill); reserve confirmation dialogs for genuinely irreversible actions and prefer easy undo everywhere else.

## Gestures & direct manipulation

- Feedback fires on pointer-down, not release: highlight/press-scale the instant of contact, and keep feedback continuous and 1:1 with the pointer for the whole drag.
- During drag: capture the pointer so tracking survives leaving the element’s bounds, respect the offset from where the user grabbed, ignore additional touch points once a drag has begun.
- Require ~10px of movement before committing to a drag direction; let a press cancel by dragging away and back before release.
- Dismiss on velocity, not distance alone: a flick above ~**0.1 px/ms** dismisses regardless of distance traveled.
- On release, project the resting position from velocity — `projection = (v/1000) × d/(1−d)` with deceleration d ≈ 0.998 — snap to the nearest target, then hand the release velocity to the settling spring so there is no seam between drag and animation.
- Rubber-band at boundaries: progressively increasing resistance past an edge, never a hard stop.
- Use springs for gesture-driven or interruptible motion — they preserve velocity across interruption; parametrize as duration + bounce (e.g. ~0.5s, bounce 0), not mass/stiffness/damping; bounce stays 0 in product UI, 0.1–0.3 only when the triggering gesture carried momentum (a flick or throw).
- Never lock out input during a transition; on interruption animate from the current on-screen (presentation) value, never the logical target.

## Motion

Before adding motion, name its purpose from a closed list: feedback, spatial continuity, state indication, preventing a jarring change, explanation, or delight (rare tier only). “It looks cool” fails. Never add decorative motion to data the user is reading or acting on (charts, tables, dense functional UI).

Grade by frequency tier:

| Tier | Examples | Motion budget |
| --- | --- | --- |
| 100+/day or keyboard-initiated | command palettes, keyboard nav | none — palettes used hundreds of times daily ship without open/close animation |
| Tens/day | hover, list navigation | near-imperceptible only |
| Occasional | modals, drawers, toasts | standard, under 300ms |
| Rare / first-run | onboarding, empty states, success | the only tier where delight (bounce, generous stagger, longer beats) is allowed |

Use `tokens.motion` when present; otherwise defaults:

| Kind | Duration | Notes |
| --- | --- | --- |
| Hover / color | 100–150ms | Soft ease |
| Tooltip / dropdown | 150–250ms | `ease-out` enter |
| Modal / drawer | 200–300ms | Under 300ms for product UI |
| Page transition | ≤ 400ms | Marketing may go longer |

Easing decision tree:

```
Entering?                        → ease-out (prefer cubic-bezier(0.32, 0.72, 0, 1)); never ease-in
Exiting?                         → ease-in, accelerating away (the only legitimate ease-in)
Moving/resizing while on screen? → ease-in-out
Hover / color / shadow?          → soft ease, ~150ms
Constant-rate (marquee, spinner,
progress-that-represents-time)?  → linear
Gesture-driven / interruptible?  → spring (duration + bounce, bounce 0)
```

Rules:

- Animate **`transform` / `opacity` only** — never width/height/margin/top/left.
- Never `transition: all` (a bare utility `transition` class compiles to it).
- Built-in keyword easings are too weak for deliberate motion — use custom cubic-beziers for entrances, exits, and on-screen movement.
- Reversible or rapidly-triggered states (open/close, toggles, hover, stacking toasts) use CSS transitions or springs, which retarget from the live position; `@keyframes` restart from zero and read as broken — reserve keyframes for run-to-completion sequences (entrances, loaders). Use `@starting-style` for JS-free entry transitions.
- Exits are ~20–30% faster than enters and asymmetric — a departure, not the entrance played backwards — but travel the same path: a surface that slid in from an edge dismisses back to that edge.
- Exits travel a small fixed distance (~8–12px) in a meaningful direction plus fade — never the element’s own height, never a directionless pure fade, never an instant cut; full off-screen slides only when the destination is itself the information (swiped-away card, closing drawer).
- Don’t enter from `scale(0)` — start ~`0.95` + opacity 0.
- Origin-aware popovers (scale from the trigger); centered modals are exempt — `transform-origin: center` is correct there.
- Paired elements that move as one unit (modal + overlay, drawer + backdrop, tooltip + arrow) share identical duration and easing.
- Never play entrance animations on elements simply at rest at first paint — reserve entrances for state changes the user causes; exception: deliberate first-run moments (staggered hero, onboarding) whose whole point is the entrance.
- State-driven icon swaps (play→pause, copy→check) cross-fade with a deep scale (~0.3→1) + opacity + slight blur (~3px→0), no bounce; a timid 0.8–0.9 scale start reads as a glitch; layer both icons so the reverse direction animates too.
- Choreograph: when several elements would move simultaneously and clash, sequence them instead of animating in parallel.
- Stagger group entrances 30–80ms per item (per-word hero text ~80ms); stagger is decorative and must never delay interactivity.
- Slow where the user is deciding, fast where the system responds: hold-to-confirm fills ~2s linear on press, snaps back ~200ms ease-out on release — symmetric timing on press-and-hold is a defect.
- Tooltips form a warm group: the first gets a hover delay and entrance; while any tooltip is open, siblings open instantly with no delay or animation; the warm state clears ~300ms after the last closes.
- If a hover animation moves the element out from under the cursor (flicker loop), animate a child and keep the parent’s hover hit area static.
- Use percentage transforms for enter/exit travel (`translateY(100%)` moves by the element’s own height) instead of hardcoded pixels.
- When a crossfade visibly double-exposes two states, bridge it with a subtle ~2px blur; keep any animated blur under 20px.
- Motion values live as shared tokens: several hand-typed near-identical cubic-beziers is a consolidation defect; new motion extends the project’s motion tokens, never a parallel set.
- Never add an animation dependency for motion CSS can express; match the project’s existing motion stack first.
- Reduced motion means gentler, not zero: remove movement and position change, keep brief opacity/color feedback that aids comprehension; autoplaying video swaps to a poster + play button.
- Disable theme-switch transition cascades when possible.
- When fixing motion, prefer remedies in order: delete → reduce (shorter, smaller, fewer properties) → fix easing → fix origin/physicality → make interruptible → move to transform/opacity → make timing asymmetric → polish (blur bridge, stagger). Deleting is often the strongest fix.
- When feel can’t be judged from code, verify in slow motion (2–5× duration or the browser’s animation inspector) and frame-by-frame; test gestures on a real device.

## Performance

- Virtualize any list that can exceed ~50 items or grow unbounded — render only what is visible.
- Never drive per-frame animation through framework state/re-renders; write transforms directly to the element (refs, WAAPI, or CSS).
- Never animate a CSS variable on a shared parent — it recalculates styles for every descendant; set the property on the moving element itself.
- Prefer compositor-driven animation (CSS/WAAPI) for predetermined motion — it stays smooth while the main thread is busy; reserve JS loops for dynamic, gesture-driven, or spring values.
- `will-change` only for compositor properties (transform, opacity, filter, clip-path), only on the animating element, and only after observing a first-frame hitch — it is also the fix for 1px start/end jitter; never routine seasoning, never `will-change: all`.
- Preload fonts and above-the-fold images; lazy-load below-the-fold media; every image and video declares dimensions or `aspect-ratio`.
- Pause looping animations, video, and timers when off-screen or the tab is hidden (IntersectionObserver / visibility events, `animation-play-state`).
- Statically pre-render content surfaces (blog, docs, changelog) at build time with revalidation — never fetch them at request time.

## Marketing / hero restraint

When `.design` `patterns` or rationale don’t specify:

- First viewport: brand, one headline, one supporting line, one CTA group, one dominant visual — no card soup, stat strips, or floating promo chips in the hero.
- Match project brand; never default to a catalogued AI look (see **Default looks to avoid**).
- Motion maps to user input: no scroll-triggered fade-ins/fade-ups, no scroll hijacking, no parallax that isn’t 1:1 with scroll position, no auto-advancing carousels.
- Intro/hero animations play once per session — gate with `sessionStorage` so internal navigation skips them but a genuinely new visit sees them.
- Hover-revealed navigation content lives in the DOM at all times (visually hidden), never mounted on hover.
- CTAs adapt to auth state: signed-out gets “Get started”, signed-in gets “Open app” — never “Sign up” to a signed-in user.

## Component APIs

- Composition over configuration; prefer catalog / shadcn primitives.
- Never hand-roll dialogs, popovers, menus, toasts, or virtualization with manual focus/dismiss handling when an accessible primitive library is available; check what the project already has installed before adding any dependency.
- After inventing an approved control, **UPDATE** `.design` `components` so the next session doesn’t fork it.
- Avoid boolean-prop explosion; support controlled + uncontrolled when state is involved.
- Layer customization in a fixed order: variants → size → `className` escape hatch → element swap; never expose raw style props (`backgroundColor`, `paddingX`, …).
- Name props the way the platform does: HTML names (`disabled`, not `isDisabled`), positive booleans (`open`, not `isNotClosed`), `on`-prefixed handlers — consistently.
- Every component wrapping a DOM element forwards its ref and spreads remaining props (`aria-*` / `data-*` pass through); button-like components default to `type="button"`.
- Compound components (context-shared parts) when parts share implicit state or children vary; a single component with few props when the structure is fixed.
- Don’t extract a shared component until the pattern has repeated two or three times.
- Tooltips contain no interactive content (links, buttons are unreachable by hover) — use a click-triggered popover instead.
- Never wrap an entire card in one `<a>` — it kills text selection and reads as one giant link; give the card a distinct CTA link.
- A switch implies immediate effect — settings that apply without a save action only; otherwise a checkbox with explicit save.
- Badge vs tag: a badge is attached and informational (counts); a tag is standalone, selectable, or removable (categories); a “New” marker is neither. Avatars always define a non-image fallback (initials or generic mark).

## Copy

- Sentence case for UI; outcome-specific button labels.
- Store copy in natural sentence case and apply casing with `text-transform`; never bake ALL-CAPS into source strings.
- Errors tell how to fix; placeholders are not labels.
- Empty states: context + next action.
- Carry action names through a flow: a “Publish” button confirms with “Published”, not a synonym.
- Use the user’s vocabulary, not internal jargon (“manage notifications”, not “webhook config”).
- Destructive confirmation dialogs describe exactly what will be lost — never just “Are you sure?”.
- Detect the platform: display and bind Cmd on macOS, Ctrl elsewhere; surface a control’s shortcut in its tooltip.
- Drop filler “please” from short imperatives.

## Information architecture

- Navigation labels use the user’s vocabulary; repeated search queries for a term the nav calls something else are a signal to rename the nav item.
- Prefer flat structure with breadcrumbs over 3+ levels of nesting; group long flat settings pages into sections with side navigation, not one scroll.
- Onboarding that creates the user’s first real item in one step beats a multi-stop feature tour.

## Default looks to avoid

Recognizable machine-generated aesthetics. These are **defaults, not choices** — when `.design` or the user explicitly claims one, it is a valid choice; when the file is silent, never spend free choices on them:

- Purple-to-blue gradient hero on a white page.
- Warm cream ground + high-contrast serif + terracotta accent.
- Near-black surface + a lone acid accent (acid green, vermilion).
- Hairline-broadsheet: hairline rules, zero radius, dense editorial columns applied everywhere.
- Uniform `rounded-lg` cards for every surface; accent bar bolted onto a rounded card.
- Emoji as section markers or list bullets.
- Everything centered, section after section.
- One safe geometric sans doing every role on the page.

The antidote is not banning ingredients — it is a committed direction: pick a specific reference, concentrate boldness in one signature element, and record the choice in `.design` so it reads as intent, not default.

## When `.design` speaks

```
CRAFT rule conflicts with tokens / constraints / rationale / when_when_not?
└── .design wins — follow the contract, note the override briefly
```
