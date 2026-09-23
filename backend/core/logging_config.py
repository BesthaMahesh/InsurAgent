import logging
import re
import sys

# PII Masking regex patterns for safe enterprise logging
EMAIL_PATTERN = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_PATTERN = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
CARD_PATTERN = re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')
AADHAAR_SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b|\b\d{4}\s\d{4}\s\d{4}\b')


class PIIMaskingFormatter(logging.Formatter):
    """Custom logging formatter to sanitize sensitive claimant data."""

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        msg = EMAIL_PATTERN.sub("[EMAIL_MASKED]", msg)
        msg = PHONE_PATTERN.sub("[PHONE_MASKED]", msg)
        msg = CARD_PATTERN.sub("[CARD_MASKED]", msg)
        msg = AADHAAR_SSN_PATTERN.sub("[ID_MASKED]", msg)
        return msg


def setup_logger(name: str = "InsurAgent") -> logging.Logger:
    """Configures structured logger with console output and PII filter."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = PIIMaskingFormatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


logger = setup_logger("InsurAgent")
