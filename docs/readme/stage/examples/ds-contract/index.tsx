import { Card, Code, Stage, Text, Window, type CodeLine } from '../../kit'
import '../_ds/ds.css'

// Built from examples/static-card: a light document window (the .design
// file open in an editor) and a detail card straddling its right edge.
// The file is the real templates/starter.DESIGN, trimmed to the four
// sections the story is about: tokens, locked, a component's when / when
// not, and voice. The card is the file's required agent.instructions,
// its four verbs. Corner bleed: inset top-left, off the bottom.
const YAML: CodeLine[] = [
  { text: 'schema: design.v1' },
  { text: 'tokens:' },
  { text: '  color:' },
  { text: '    primary: "#0B57D0"' },
  { text: '    on-primary: "#FFFFFF"' },
  { text: '  radius: { sm: 6, md: 10, pill: 9999 }' },
  { text: 'locked:' },
  { text: '  - tokens.color.primary' },
  { text: 'components:' },
  { text: '  button:' },
  { text: '    when: ["primary and secondary actions"]' },
  { text: '    when_not: ["inventing off-system chrome"]' },
  { text: 'voice:' },
  { text: '  casing: sentence' },
]

const VERBS: [string, string][] = [
  ['Read', 'The normative core first'],
  ['Follow', 'Tokens, components, voice'],
  ['Update', 'In place; ask on a locked path'],
  ['Verify', 'Drift by token group'],
]

export default function Contract() {
  return (
    <Stage width={800} height={372} className="de ds-contract">
      {() => (
        <>
          <Window title="relay.DESIGN" className="de-win de-card-win ds-editor" style={{ width: 600, height: 420 }}>
            <Code lines={YAML} highlight={false} className="ds-yaml" />
          </Window>
          <Card className="de-sat ds-contract__card" pad="small" gap={2}>
            <div className="ds-card__head">
              <Text className="de-mono de-strong">agent.instructions</Text>
              <Text className="de-label">required</Text>
            </div>
            {VERBS.map(([verb, what]) => (
              <div key={verb} className="ds-verb">
                <Text className="de-h">{verb}</Text>
                <Text className="de-sub">{what}</Text>
              </div>
            ))}
          </Card>
        </>
      )}
    </Stage>
  )
}
