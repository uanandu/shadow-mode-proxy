# Redaction of keys or anything before write is applied

import re


KNOWN_SECRET_FORMATS = [
    # AWS access key ID (permanent + temporary/session)
    re.compile(r'\b((?:AKIA|ASIA)[0-9A-Z]{16})\b'),
    # GCP API key
    re.compile(r'\b(AIza[0-9A-Za-z\-_]{35})\b'),
    # Azure Storage connection string account key
    re.compile(r'(?i)(AccountKey=)([A-Za-z0-9/+=]{20,})'),
    # Private key blocks (any provider)
    re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----'),
]

# labeled flag/env/assignment forms used across aws/az/gcloud CLIs
GENERIC_ASSIGNMENT = re.compile(
    r'(?i)(--)?\b('
    r'api[_-]?key|secret|token|password|credential|'
    r'access[_-]?key|secret[_-]?key|client[_-]?secret'
    r')s?\b([\s=:]+)(\S+)'
)

# Redaction function to replace pattern with [REDACTED]
def redact_text(input_text: str) -> str:
    for pattern in KNOWN_SECRET_FORMATS:
        input_text = pattern.sub("[REDACTED]", input_text)
    input_text = GENERIC_ASSIGNMENT.sub(r'\1\2\3[REDACTED]', input_text)
    return input_text

# Gitignore enforcement and ensuring that we have only one decision per call
def correlation_id(event: dict) -> str:
    return f"{event.get('session_id')}:{event.get('tool_use_id')}"
