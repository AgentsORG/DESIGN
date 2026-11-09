import { Code, Prompt, Stage, Window, type CodeLine } from '../../kit'
import { Input, Turn } from '../_ds/claude'
import '../_ds/ds.css'

// Built from examples/ai-chat inside examples/hero-demo's Claude Code
// terminal, the same review shape as the design-engineering README's
// de-review still: /design-engineering reads the project's .design first
// and ranks it above its own defaults, so the review has two kinds of
// finding: contract drift (the .design owns the value) and craft (the
// skill owns the rule). Corner bleed: inset top-left, off right and bottom.
const FINDINGS: [number, CodeLine[]][] = [
  [12, [
    { text: 'background: #2563eb;', kind: 'del' },
    { text: 'background: var(--color-primary);', kind: 'add' },
    { text: '// tokens.color.primary is locked in relay.DESIGN', number: false },
  ]],
  [27, [
    { text: '<Button>Start Free Trial</Button>', kind: 'del' },
    { text: '<Button>Start free trial</Button>', kind: 'add' },
    { text: '// voice.casing: sentence (relay.DESIGN)', number: false },
  ]],
  [41, [
    { text: 'transition: all .3s ease-in;', kind: 'del' },
    { text: 'transition: transform 150ms var(--easing-enter);', kind: 'add' },
    { text: '// Name the property, enter on ease-out. [[easing-curves]]', number: false },
  ]],
]

export default function Pair() {
  return (
    <Stage width={800} height={460} className="de ds-pair">
      {() => (
        <Window chrome="terminal" title="relay — claude" className="de-win" style={{ width: 800, height: 480 }}>
          <div className="ss-term de-term">
            <Prompt path="~/relay">claude</Prompt>
            <div className="w">{'> /design-engineering review app/pricing/page.tsx'}</div>
            <div className="gap" />
            <Turn>Contract: relay.DESIGN (design.v1). It outranks my defaults.</Turn>
            <Turn>Two contract drifts and one craft fix. Before (−), After (+), Why:</Turn>
            {FINDINGS.map(([start, lines]) => <Code key={start} lines={lines} start={start} highlight={false} />)}
            <div className="gap" />
            <Turn>Verdict: ship after these three.</Turn>
            <Input />
          </div>
        </Window>
      )}
    </Stage>
  )
}
