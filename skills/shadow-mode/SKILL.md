---
name: shadow-mode
description: Toggle shadow mode on or off for this session
disable-model-invocation: true
---

The user ran /shadow-mode-proxy:shadow-mode with argument "$ARGUMENT".

If the argument is "on":
- Create the fle ${CLAUDE_PLUGIN_DATA}/shadow-mode.flag (empty file; create the directory if it does not exist)
- Confirm to user: "Shadow mode is ON - risky tool calls will be logged, not executed"

If the argument is "off":
- Delete ${CLAUDE_PLUGIN_DATA}/shadow-mode.flag if it exists
- Confirm to the user: "Shadow mode is ON - tool calls will run normally"

IF the argument is anything else, ask the user to verify: "on" or "off"
