import json, sys, os, datetime
from _common import redact, correlation_id

# Absolute Path to enable saving log in the project root regardless of the directory
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
LOG_PATH = os.path.join(PROJECT_DIR, "shadow-log.jsonl")
GITIGNORE_ENTRY = "shadow-log.jsonl"

# checks for gitignore and if it isnt then it appends it before any log entry is writted (side effect fix)
def _ensure_gitignore():
    # Only touch .gitignore if PROJECT_DIR is actually a git repo root
    if not os.path.isdir(os.path.join(PROJECT_DIR, ".git")):
        return

    gitignore_path = os.path.join(PROJECT_DIR, ".gitignore")
    existing = ""
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            existing = f.read()

    if GITIGNORE_ENTRY in existing.splitlines():
        return

    with open(gitignore_path, "a") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write(GITIGNORE_ENTRY + "\n")

def write_log(event: dict, decision: str, source: str) -> dict:
    _ensure_gitignore()
    record = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
        "correlation_id": correlation_id(event),
        "tool_name": event.get("tool_name"),
        "tool_input": redact(event.get("tool_input")),
        "decision": decision,
        "source": source,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")
    return record