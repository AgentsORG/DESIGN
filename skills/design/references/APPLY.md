# APPLY — decision procedures for following `.design`

Encode process, not vibes. Walk these trees the same way every run.

## Component reuse

```
Need a control?
├── Exact components.* match for the interaction?
│   └── Yes → use it (respect import path if present)
└── Partial match (same role, missing variant)?
    ├── policy.reuse.prefer_existing_components?
    │   └── Yes → extend via proposal (new variant), do not fork a second Button
    └── if_missing
        ├── ask → stop and ask
        ├── nearest → closest component + note in PR/summary
        └── invent_with_note → one-off + update .design catalog
```

## Button (and similar CTA) selection

If `decisions.button` exists, walk it first. Otherwise default tree:

```
Is the action destructive (delete, revoke, irreversible)?
├── Yes → danger / destructive variant
└── No
    ├── Is it the single primary action of the view?
    │   ├── Yes → filled / primary (constraints: one per view)
    │   └── No
    │       ├── Secondary alternative (cancel, back)?
    │       │   └── outlined / secondary / ghost per catalog
    │       └── Tertiary / inline → ghost or link style per catalog
```

## Token binding

```
Need a color / space / radius / type style?
├── Semantic token exists?
│   └── Yes → use {tokens.*} or the project's CSS var mapped from it
└── No
    └── fallback_order
        ├── semantic_token → fail closed / ask
        ├── nearest_approved_token → closest scale step + note
        └── ask → ask user
```

Never introduce raw hex/rgb when a token exists (`constraints.always`).

## Component property bags (DESIGN.md)

```
Implementing a catalog / flat component?
├── Read tokens.<variant> OR flat property bag
├── For each of backgroundColor, textColor, typography, rounded,
│   padding, size, height, width (and extensions): apply exactly
├── Apply *-hover / *-active / *-focus sibling entries when present
├── Read rationale.components for craft rules tokens omit
└── Do NOT drop unknown properties — preserve on UPDATE
```

Aliases: `background`≡`backgroundColor`, `foreground`≡`textColor`, `radius`≡`rounded`.

## Spacing

```
Spacing decision?
├── tokens.spacing.unit defined?
│   └── Yes → snap to multiples of unit (and named sm/md/lg when listed)
└── Prefer gap on parents over per-child margins
```

If `policy.responsive.if_mobile` says `reduce_padding_before_font_size`, shrink spacing tokens before reducing body font size.

## Hierarchy tradeoffs

Apply `policy.hierarchy` in order (default: typography → spacing → contrast → color). When two rules conflict, preserve earlier items first.

## Craft gates (when `.design` is silent)

Before finishing UI generation, apply [CRAFT.md](CRAFT.md):

```
After binding tokens + components
├── One clear primary CTA?
├── States covered (hover/focus/disabled/loading/empty/error)?
├── Nested radii computed (inner = outer − padding)?
├── Motion: transform/opacity only, <300ms, reduced-motion honored?
├── Tap targets ≥ 44×44; focus visible; inputs ≥ 16px on mobile?
├── Body measure ~65ch; gap on parents; no hover-only core actions?
└── Marketing hero restrained unless patterns.* say otherwise?
```

If a CRAFT rule conflicts with tokens / constraints / rationale / when_when_not → **`.design` wins**.

## Component API (invent path)

When `policy.if_missing` allows inventing:

- Prefer composition (slots/children) over boolean-prop piles
- Prefer existing catalog / shadcn primitives over a new parallel Button
- After user accepts the control, UPDATE `.design` `components` in the same task when asked to persist design progress

## Pattern surfaces

```
Building a named surface (hero, dashboard, settings)?
├── patterns.<name> exists?
│   ├── Use only allowed parts
│   ├── Omit forbidden parts
│   └── Honor prioritize hints (e.g. table over cards when dense)
└── No pattern → compose from components + constraints only
```

## Styling system

Detect the project's approach (Tailwind, CSS modules, vanilla-extract, etc.). Map `.design` values into that system. Never switch the stack mid-task.

## shadcn/ui

```
integrations.shadcn.enabled?
├── No → styling system path above
└── Yes
    ├── Prefer components under aliases.ui (install via shadcn CLI if missing)
    ├── Ensure components.json has cssVariables: true
    ├── Resolve theme:
    │   ├── css_vars.light / .dark present? → use them
    │   └── else derive from map_from_tokens → tokens.*
    ├── Write :root and .dark variables into integrations.shadcn.css
    ├── Set --radius from integrations.shadcn.radius (or tokens.radius)
    └── If tokens disagree with css_vars → tokens win; update css_vars + CSS
```

Still obey `components.*` when/when_not and `constraints` — shadcn is the implementation vehicle, not a free pass to ignore the catalog.

Docs: [docs/shadcn.md](../../../docs/shadcn.md) · Spec: [SPEC.md §7.1](../../../SPEC.md).
