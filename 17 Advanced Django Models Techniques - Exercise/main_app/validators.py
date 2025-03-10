from django.core.exceptions import ValidationError


def name_validator(value: str):
    if not value.replace(" ", "").isalpha():
        raise ValidationError("Name can only contain letters and spaces")


def phone_number_validator(value: str):
    if value[:4] != '+359' or not value[4:].isdigit() or len(value) != 13:
        raise ValidationError("Phone number must start with '+359' followed by 9 digits")


