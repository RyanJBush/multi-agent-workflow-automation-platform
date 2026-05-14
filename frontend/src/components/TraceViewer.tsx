import { useMemo, useState } from "react"

export interface TraceStep {
  agent_name: string
  input: string
  output: string
  tool_calls: string[]
  latency_ms: number
  token_count: number
  timestamp: string
}

export function TraceViewer({ steps }: { steps: TraceStep[] }) {
  const [open, setOpen] = useState<Record<number, boolean>>({})
  const color = (latency: number) => latency < 500 ? '#166534' : latency < 2000 ? '#a16207' : '#b91c1c'
  const ordered = useMemo(() => [...steps], [steps])
  return <div className="panel"><h3>Trace Viewer</h3>{ordered.map((s, i) => <div key={i} style={{borderLeft:'2px solid #cbd5e1', paddingLeft:12, marginBottom:10}}><button onClick={()=>setOpen({...open,[i]:!open[i]})}>{open[i]?'▾':'▸'} {s.agent_name} • <span style={{color:color(s.latency_ms)}}>{s.latency_ms}ms</span></button>{open[i] && <div><p><strong>Input:</strong> {s.input}</p><p><strong>Output:</strong> {s.output}</p><p><strong>Tool calls:</strong> {s.tool_calls.join(', ')||'none'}</p></div>}</div>)}</div>
}
