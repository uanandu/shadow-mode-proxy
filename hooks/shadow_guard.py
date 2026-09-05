import json, sys, os, datetime

def main():        
    # Claude sends tool call as JSON on stdin before it runs
    event = json.load(sys.stdin)
    
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