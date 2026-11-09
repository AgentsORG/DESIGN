import { Card, Code, Prompt, Stage, Text, Window, type CodeLine } from '../../kit'
import '../_ds/ds.css'

// Built from examples/static-card with examples/hero-demo's terminal as
// the hero: the reference exporter run on the starter template, its real
// output (paths shortened to the project), and a satellite card with the
// first lines of the CSS it wrote. Corner bleed: inset top-left, off the
// bottom; the card straddles the terminal's right edge.
const WROTE: [string, string][] = [
  ['css', 'src/styles/tokens.css'],
  ['tailwind', 'tailwind.theme.css'],
  ['dtcg', 'tokens/tokens.json'],
  ['shadcn_registry', 'registry/brand-theme.json'],
  ['frame_md', 'frame.md'],
]

const CSS: CodeLine[] = [
  { text: ':root {' },
  { text: '  --color-primary: #0B57D0;' },
  { text: '  --color-on-primary: #FFFFFF;' },
  { text: '  --color-surface-base: #F8FAFC;' },
  { text: '  --radius-md: 10px;' },
  { text: '  --spacing-md: 16px;' },
  { text: '}' },
]

export default function Exports() {
  return (
    <Stage width={800} height={340} className="de ds-exports">
      {() => (
        <>
          <Window chrome="terminal" title="relay — zsh" className="de-win" style={{ width: 600, height: 380 }}>
            <div className="ss-term de-term">
              <Prompt path="~/relay">python scripts/export_design.py relay.DESIGN</Prompt>
              {WROTE.map(([kind, path]) => (
                <div key={kind}><span className="dim">wrote </span><span className="w">{kind.padEnd(16)}</span><span className="a">{path}</span></div>
              ))}
              <div className="gap" />
              <Prompt path="~/relay" />
            </div>
          </Window>
          <Card className="de-sat ds-exports__card" pad="small" gap={6}>
            <div className="ds-card__head">
              <Text className="de-mono de-strong">tokens.css</Text>
              <Text className="de-label">generated, never edited</Text>
            </div>
            <Code lines={CSS} highlight={false} numbers={false} className="ds-css" />
          </Card>
        </>
      )}
    </Stage>
  )
}
