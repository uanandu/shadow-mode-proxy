import json, sys, os, datetime

# For the ON/OFF switch
PLUGIN_DATA = os.environ.get("CLAUDE_PLUGIN_DATA")
print(f"PLUGIN_DATA")
FLAG_PATH = os.path.join(PLUGIN_DATA, "shadow-mode.flag") if PLUGIN_DATA else None

def main():        
    # Claude sends tool call as JSON on stdin before it runs
    event = json.load(sys.stdin)
    
    # Here we set the shadow mode off permission decision reason to Claude
    # No FLAG_PATH set or flag file is missing -> shadow mode is off -> allow tool, skip blocking logic and exit early
    if not FLAG_PATH or not os.path.exists(FLAG_PATH):
        print(f"PLUGIN_DATA={PLUGIN_DATA!r} FLAG_PATH={FLAG_PATH!r}", file=sys.stderr)
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "shadow mode is off"
            }
        }))
        return
    
    # Tool name and tool input from the event 
    tool_name = event.get("tool_name")
    tool_input = event.get("tool_input")
    
    # Record set for the shadow-log.jsonl
    record = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "tool_name": tool_name,
        "tool_input": tool_input,
        "decision": "deny",
        "source": os.path.basename(__file__),
    }
    
    # Append the record in shadow-log.jsonl
    with open("shadow-log.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")
    
    print(
        json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"Shadow mode is on — {tool_name} was NOT run. "
                    f"Logged to shadow-log.jsonl instead."
                )
            }
        })
    )
    
if __name__ == "__main__":
    main()