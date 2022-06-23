import re

SUBSCRIPTION_DEFAULTS = {
            "tempCelsiusAbove": None,
            "tempCelsiusBelow": None,
            "weatherCodeEquals": None,
            "windSpeedExceeds": None,
        }

API_ROOT_TEXT = "Weather monitor API root"

INVALID_EMAIL_MESSAGE = "Email is not in a valid format"
valid_email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_valid_email(email: str) -> bool:
    return True if re.fullmatch(valid_email_regex, email) else False
