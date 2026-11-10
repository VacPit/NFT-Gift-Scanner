import logging
import re

# Маскируем то, что не должно попадать в логи: токены бота и initData.
_SECRET_PATTERNS = [
    (re.compile(r"\b\d{6,}:[A-Za-z0-9_-]{30,}\b"), "[bot-token]"),
    (re.compile(r"(init_?data=)[^\s&]+", re.IGNORECASE), r"\1[redacted]"),
    (re.compile(r"(authorization:\s*bearer\s+)\S+", re.IGNORECASE), r"\1[redacted]"),
]


class RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        for pattern, replacement in _SECRET_PATTERNS:
            message = pattern.sub(replacement, message)
        record.msg, record.args = message, None
        return True


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    handler.addFilter(RedactingFilter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
