import json, sys, os, datetime

# Absolute Path to enable saving log in the project root regardless of the directory
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
LOG_PATH = os.path.join(PROJECT_DIR, "shadow-log.jsonl")

def main():
    # Claude sends tool call as JSON on stdin before it runs
    event = json.load(sys.stdin)

    # append-only audit trail, one JSON object per tool call
    with open(LOG_PATH, "a") as f:
        record = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "tool_name": event.get("tool_name"),
            "tool_input": event.get("tool_input"),
             "decision": "allow",
            "source": os.path.basename(__file__),
        }
        f.write(json.dumps(record) + "\n")
        
    # always allow: this hooks only observes
    # shadow_guard.py does the blocking
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "logging only - not yet blocking anything",
        }
    }))
    
if __name__ == "__main__":
    main()