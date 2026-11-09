import { Card, Prompt, Row, Stage, Text, Window } from '../../kit'
import { Input, Result, Turn } from '../_ds/claude'
import '../_ds/ds.css'

// Built from examples/static-card (a hero window and a detail card that
// straddles its edge, one row selected) with examples/hero-demo's Claude
// Code terminal as the hero. The story: a .design file is dropped into the
// chat, the agent reads it, and builds with its tokens and voice. The card
// is the part of the contract the build bound to, the locked token first.
// Corner bleed: the terminal is inset top-left and runs off the bottom;
// the card straddles its right edge, a gutter from the stage's right edge.
const BOUND: [string, string, string][] = [
  ['color.primary', '#0B57D0', 'locked'],
  ['radius.md', '10', ''],
  ['spacing.unit', '4', ''],
  ['voice.casing', 'sentence', ''],
]

export default function Drop() {
  return (
    <Stage width={800} height={372} className="de ds-drop">
      {() => (
        <>
          <Window chrome="terminal" title="relay — claude" className="de-win" style={{ width: 600, height: 420 }}>
            <div className="ss-term de-term">
              <Prompt path="~/relay">claude</Prompt>
              <div className="w">{'> @relay.DESIGN build the pricing page'}</div>
              <div className="gap" />
              <Turn tool><span className="w">Read</span>(relay.DESIGN)</Turn>
              <Result>design.v1 · relay 1.3.0 · 3 locked</Result>
              <div className="gap" />
              <Turn>Following its agent.instructions:</Turn>
              <div>{'  tokens are normative, voice on every label.'}</div>
              <div className="gap" />
              <Turn tool><span className="w">Write</span>(app/pricing/page.tsx)</Turn>
              <Result>0 raw hex · 0 invented spacing · Button and Card from the catalog</Result>
              <Input />
            </div>
          </Window>
          <Card className="de-sat ds-drop__card" pad="small" gap={2}>
            <div className="ds-card__head">
              <Text className="de-mono de-strong">relay.DESIGN</Text>
              <Text className="de-label">what the build bound to</Text>
            </div>
            {BOUND.map(([path, value, flag], i) => (
              <Row
                key={path}
                pad={6}
                selected={i === 0}
                title={<Text className="de-mono">{path}</Text>}
                meta={<span className="ds-val"><Text className="de-mono">{value}</Text>{flag && <span className="ds-flag">{flag}</span>}</span>}
              />
            ))}
          </Card>
        </>
      )}
    </Stage>
  )
}
