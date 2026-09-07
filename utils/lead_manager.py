import re


def is_valid_phone(phone):

    phone = phone.replace(" ", "")

    pattern = r"^[6-9]\d{9}$"

    return bool(re.match(pattern, phone))


def is_valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(re.match(pattern, email))