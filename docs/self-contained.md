# Canonical `agent.instructions` (self-contained)

Every `.design` file MUST embed enough procedure that an agent can use it after a drag-drop or `@`-mention **without** installing the portable skill. Normative copy lives in [SPEC.md §8](../SPEC.md).

Recommended block (adapt brand disclaimer as needed):

```yaml
agent:
  skill: design
  instructions: |
    You are holding a .design living visual contract (schema design.v1).
    If the AgentsORG `design` skill is installed, activate it — then still obey THIS file as source of truth.
    If the skill is absent, follow these instructions exactly.

    READ
    - Load this file before any UI generation or restyle. Large file? Normative core first
      (intent, constraints, policy/decisions, tokens, components, themes, voice, locked); rationale on demand.
    - Order: overview/intent → constraints → policy/decisions → tokens → voice → rationale → components/patterns → integrations → locked.
    - Tokens and structured rules are normative. Rationale is judgment when tokens under-specify.

    FOLLOW (generate or edit UI)
    - Calibrate treatment per surface: patterns.<name>.treatment > intent.treatment
      (utilitarian = restrained product craft; editorial = distinctive identity).
    - Prefer catalog components; obey when / when_not and decisions.* (first match wins).
    - Bind every listed component property (backgroundColor, textColor, typography, rounded, padding, size, height, width).
    - Never invent raw hex/spacing/radius when a token exists.
    - Apply patterns.*; enforce constraints.always / never; apply voice.* to all UI copy.
    - Concentrate boldness in intent.signature; keep everything around it quiet.
    - Themes: generate for the active mode (themes.default); modes are designed, never inverted.
    - Match the project's existing styling stack — do not switch stacks.
    - If integrations.shadcn.enabled: prefer shadcn UI; write css_vars into the listed CSS file; tokens win on conflict.
    - If integrations.figma is present: this file is repo-canonical unless sync.direction says otherwise; ask on conflicts.
    - Craft defaults when this file is silent: one primary CTA; nested radius = outer − padding; transform/opacity only (<300ms); 44×44 targets; focus visible; prefers-reduced-motion; no transition:all.

    UPDATE
    - Edit this file in place when design changes. Git is history.
    - Ask before changing any path in locked. Bump version (SemVer).

    VERIFY
    - Compare tokens ↔ CSS/Tailwind and components ↔ imports; report drift per token group
      as added/removed/modified plus a regression flag before fixing.

    PRECEDENCE
    1) User prompt  2) This file  3) design skill  4) Generic taste skills  5) Model defaults

    NEVER
    - Invent a parallel design system beside this file
    - Embed binaries or full page HTML trees here
    - Claim affiliation with third-party brands used only as visual references
```

Brand-analysis examples append one extra section (generic files omit it):

```text
DISCLAIMER
Independent visual analysis - not affiliated with the named brand. Adapt before production use.
```

This block is byte-identical (modulo ASCII vs typographic arrows) with SPEC §8, `scripts/convert_getdesign.py` `SELF_CONTAINED_INSTRUCTIONS`, and every shipped `.design` file; `scripts/patch_agent_instructions.py` re-stamps all files from the converter constant when the template changes.
