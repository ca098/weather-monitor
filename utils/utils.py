import re
import enum

SUBSCRIPTION_DEFAULTS = {
    "tempCelsiusAbove": None,
    "tempCelsiusBelow": None,
    "weatherCodeEquals": None,
    "windSpeedExceeds": None,
}

API_ROOT_TEXT = "Weather monitor API root"

INVALID_EMAIL_MESSAGE = "Email is not in a valid format"
valid_email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class HttpStatus(enum.IntEnum):
    OKAY = 200
    CREATED = 201

    UNAUTHORIZED = 401
    FORBIDDEN = 403

    ERROR = 500


def is_valid_email(email: str) -> bool:
    return True if re.fullmatch(valid_email_regex, email) else False
