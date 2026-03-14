import re


_SENSITIVE_PATTERNS = [
    (
        re.compile(r"(Bearer\s+)([A-Za-z0-9\-._~+/]+=*)", re.IGNORECASE),
        r"\1[REDACTED]",
    ),
    (
        re.compile(r"([?&]key=)([^&\s]+)", re.IGNORECASE),
        r"\1[REDACTED]",
    ),
    (
        re.compile(r"((?:x-goog-api-key|api[_-]?key|authorization)\s*[:=]\s*)([^\s,;]+)", re.IGNORECASE),
        r"\1[REDACTED]",
    ),
    (
        re.compile(r"(AIza[0-9A-Za-z\-_]{10,})"),
        r"[REDACTED]",
    ),
]


def redact_sensitive_text(value: str) -> str:
    if not value:
        return value

    redacted = value
    for pattern, replacement in _SENSITIVE_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted
