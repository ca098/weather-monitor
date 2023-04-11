import enum
import re

SUBSCRIPTION_DEFAULTS = {
    "tempCelsiusAbove": None,
    "tempCelsiusBelow": None,
    "weatherCodeEquals": None,
    "windSpeedExceeds": None,
}

API_ROOT_TEXT = "Weather monitor API root"

INVALID_EMAIL_MESSAGE = "Email is not in a valid format"
valid_email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

EMAIL_SERVICE_REFRESH_DEFAULT = 3600

DEFAULT_CACHE_TIMEOUT = 10800  # 3 Hours


class HttpStatus(enum.IntEnum):
    OKAY = 200
    CREATED = 201

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404

    SERVER_ERROR = 500


def is_valid_email(email: str) -> bool:
    return bool(re.fullmatch(valid_email_regex, email))
