---
name: shadow-report
description: Reports a summary of what the shadow mode has blocked so far, read live from shadow-log.jsonl (a project-wide, cross-session log). Call this BEFORE answeing any questions like "what would you have done differently", "what would have happened", "what has shadow mode blocked", "show me the shadow report", "what got blocked" etc - never answer these from memor.reasoning, the log is the only source of truth.
---

Read shadow-log.jsonl in the current directory (if it doesnt exist, say that nothing has been logged yet)

For each entry, note the tool name and a short english description of what it would have done (e.g. a Bash entry running "rm -rf build/" becomes "would have deleted the build/ directory").

Only include entries where "decision" is "deny" (the calls shadow mode actually block). Entries with "decision": "allow" run normally and hence these should not appear in the report.

Present the results in the following format:

***Shadow Mode Report***

If the file shadow-log.jsonl does not exist, or has no "deny" entries, say: "Shadow mode hasn't blocked any tool calls yet"

Otherwise, list the blocked tool calls in the following chronological order:

1. **<tool_name>** at <ts, formatted HH:MM:SS UTC> — <short english description>
   `<the key command/input, e.g. tool_input.command for Bash, tool_input.file_path for Write/Edit>`
2. ...

End with: "N tool call(s) blocked this session."