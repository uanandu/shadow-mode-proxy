# Shadow-mode-proxy

Preview what a risky tool call would do before it runs.

> **Status:** functional, early release. Tool-call logging and shadow-mode blocking are both implemented. See [Limitations](#limitations) below before relying on it.

## Use case

`shadow-mode-proxy` is a Claude Code plugin that hooks into `PreToolUse` to observe and gate tool calls before they execute.

Every tool call gets logged to an append-only audit trail regardless of mode. On top of that, you can flip on **shadow mode** for a session: while it's on, risky calls (`Bash`, `Write`, `Edit`) are intercepted and logged as "would have run" instead of actually executing — so you can review exactly what Claude was about to do before trusting it to actually do it.

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
shadow_guard.py → shadow mode on? ──no──▶ allow
│
yes
│
▼
deny + log "would have run" instead of running it

```

Shadow mode is a per-session on/off switch, backed by a flag file at `${CLAUDE_PLUGIN_DATA}/shadow-mode.flag`. It's toggled through a skill rather than edited by hand.

## Installation

1. **Add the marketplace:**

```
/plugin marketplace add uanandu/shadow-mode-proxy
```

(or the full URL: `/plugin marketplace add https://github.com/uanandu/shadow-mode-proxy`)

2. **Install the plugin:**

```
/plugin install shadow-mode-proxy@anandu-shadow-mode-marketplace
```

That's it — no restart needed, the plugin is active immediately.

## Usage

### Toggle shadow mode

```
/shadow-mode-proxy:shadow-mode on
/shadow-mode-proxy:shadow-mode off
```

or

```
/shadow-mode-proxy:shadow-mode
```

and it will ask you for ```on``` or ```off```

Two scenarios:
-  **on** : `Bash`, `Write`, and `Edit` calls are intercepted and logged instead of executed. 

- **off** : everything runs normally; calls are still logged but not blocked.

### See what got blocked

No command needed. You just need to ask. e.g.:

> "What has shadow mode blocked so far?"
> "What would you have done differently?"
> "Show me the shadow report"

Claude reads `shadow-logs.jsonl` live and reports every intercepted call in Plain English.

e.g.: *"Bash - would have deleted the `build/` directory."*

## Requirements

- Claude COde with plugin support
- Python3 (for hook scripts - also no extra packages needed, standard library only)

## Limitaions

This is an early stage plugin - a few things are important to be kept in mind before you rely on it:

- **Guarded tools are limited to `Bash`, `Write`, and `Edit`.** Other tools that can have side effects (e.g. `NotebookEdit`, MCP tools) aren't intercepted.

- **The control-file allowlist check is currently a broad match**, not an exact one — the check that lets the shadow-mode toggle itself flip on/off without being blocked isn't as narrowly scoped as it should be. Treat shadow mode as a strong deterrent/audit trail, not a hard security boundary, until this is tightened.

- **The log is project-scoped, not session-scoped.** `shadow-log.jsonl` lives at the project root and accumulates across all sessions in that project — if you run multiple sessions against the same project, the log (and the shadow-report skill's "N tool call(s) blocked this session" count) reflects all of them, not just your current one.

- **No automated tests yet.**

## License

MIT — see [LICENSE](LICENSE).

