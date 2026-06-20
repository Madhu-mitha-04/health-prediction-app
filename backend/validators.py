import re
from datetime import date, datetime

# Basic, practical email regex (covers standard formats without being
# overly strict like full RFC 5322).
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_email(email):
    """
    Validate email format.
    Rejects: missing value, wrong type, no '@', no domain, no TLD.
    """
    if not email or not isinstance(email, str):
        return False, "Email is required."

    email = email.strip()

    if not EMAIL_REGEX.match(email):
        return False, "Invalid email address format."

    return True, None


def validate_date_of_birth(date_of_birth):
    """
    Validate date of birth.
    Accepts a date object or an ISO 'YYYY-MM-DD' string.
    Rejects: missing value, unparsable string, future date.
    """
    if not date_of_birth:
        return False, "Date of birth is required."

    # Normalise to a date object if a string was passed in
    if isinstance(date_of_birth, str):
        try:
            parsed_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            return False, "Date of birth must be in YYYY-MM-DD format."
    elif isinstance(date_of_birth, date):
        parsed_date = date_of_birth
    else:
        return False, "Date of birth must be a valid date."

    if parsed_date > date.today():
        return False, "Date of birth cannot be a future date."

    return True, None


def _validate_numeric_field(value, field_name):
    """
    Shared helper for glucose / haemoglobin / cholesterol:
    must be present, numeric, and >= 0.
    """
    if value is None or value == "":
        return False, f"{field_name} is required."

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return False, f"{field_name} must be a numeric value."

    if numeric_value < 0:
        return False, f"{field_name} cannot be negative."

    return True, None


def validate_glucose(glucose):
    """Validate glucose: required, numeric, >= 0."""
    return _validate_numeric_field(glucose, "Glucose")


def validate_haemoglobin(haemoglobin):
    """Validate haemoglobin: required, numeric, >= 0."""
    return _validate_numeric_field(haemoglobin, "Haemoglobin")


def validate_cholesterol(cholesterol):
    """Validate cholesterol: required, numeric, >= 0."""
    return _validate_numeric_field(cholesterol, "Cholesterol")


def validate_full_name(full_name):
    """
    Bonus validation (not explicitly listed but required by the PDF's
    'Full Name' field) - ensures it's a non-empty string.
    """
    if not full_name or not isinstance(full_name, str) or not full_name.strip():
        return False, "Full name is required."
    return True, None


def validate_patient_payload(data):
    """
    Runs all field validators against an incoming request payload (dict).
    Returns (is_valid: bool, errors: dict) where `errors` maps
    field name -> error message, suitable for a JSON API error response.
    """
    errors = {}

    is_valid, msg = validate_full_name(data.get("full_name"))
    if not is_valid:
        errors["full_name"] = msg

    is_valid, msg = validate_date_of_birth(data.get("date_of_birth"))
    if not is_valid:
        errors["date_of_birth"] = msg

    is_valid, msg = validate_email(data.get("email"))
    if not is_valid:
        errors["email"] = msg

    is_valid, msg = validate_glucose(data.get("glucose"))
    if not is_valid:
        errors["glucose"] = msg

    is_valid, msg = validate_haemoglobin(data.get("haemoglobin"))
    if not is_valid:
        errors["haemoglobin"] = msg

    is_valid, msg = validate_cholesterol(data.get("cholesterol"))
    if not is_valid:
        errors["cholesterol"] = msg

    return (len(errors) == 0), errors