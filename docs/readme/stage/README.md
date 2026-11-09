# README scenes

The stills in `../img/` are faux product UI built with a trimmed copy of
[Stageshow](https://github.com/benjitaylor/skills) (MIT, Benji Taylor). Each
scene is `examples/<name>/index.tsx`; `examples/_ds/` holds the shared look
(`ds.css`) and Claude Code's TUI marks (`claude.tsx`). The project in every
scene is a made-up product, `relay`, with its contract `relay.DESIGN`; the
token values are the real ones from `templates/starter.DESIGN`.

| Still | Scene | Built from |
|---|---|---|
| `ds-drop.png` | an agent handed `relay.DESIGN` builds a page, and what it bound to | static-card, hero-demo terminal |
| `ds-pair.png` | `/design-engineering review` ranking the contract above its own defaults | ai-chat, kit `Code` diff lines |
| `ds-contract.png` | the file in an editor, and its four `agent.instructions` verbs | static-card |
| `ds-exports.png` | `scripts/export_design.py` and the CSS it wrote (its real output) | static-card, hero-demo terminal |

## Re-render

Needs Node 20.19+ and Google Chrome (or `CHROME_PATH`).

```bash
cd docs/readme/stage && npm install
npm run dev &    # capture route on http://127.0.0.1:4711/?capture=<scene>
node scripts/film.mjs "http://127.0.0.1:4711/?capture=ds-drop" --still --gate --pad 0 --out ../img/ds-drop.png   # ends "rehearsal passed"
node scripts/layout.mjs "http://127.0.0.1:4711/?capture=ds-drop" --strict                                         # text fits its boxes
npm run typecheck
```

Stages are 800 px wide, so stills come out 1600 px wide at 2x. The scenes
are static, so `jumps.mjs` and a film's motion checks don't apply.
`node_modules/` and build output stay untracked (see the root `.gitignore`).
