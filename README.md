# Shadow-mode-proxy

Preview what a risky tool call would do before it runs.

> **Status: early scaffold.** Tool-call logging is live. The actual shadow/guard logic, both skills, and the marketplace manifest are stubs

## Use case

`shadow-mode-proxy` is a Claude Code plugin that hooks into `PreToolUse` to observe and gate tool calls before they execute.

## How it works

Both hooks run on every `PreToolUse` event, in order:

| Hook | Matcher | File | Status |
|---|---|---|---|
| Logger | `*` | [`hooks/log_only.py`](hooks/log_only.py) | Active — always allows, writes an audit record |
| Shadow guard | `Bash\|Write\|Edit` | [`hooks/shadow_guard.py`](hooks/shadow_guard.py) | Stub — not implemented |

```
tool call
  │
  ▼
log_only.py     → append record to shadow-log.jsonl → allow
  │
  ▼
shadow_guard.py → (planned) preview/block risky calls
```