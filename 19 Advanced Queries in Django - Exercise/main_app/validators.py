from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class RangeValidator:
    def __init__(self, min_value: float | int, max_value: float | int, message: str):
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    def __call__(self, value: float | int):
        if not (self.min_value <= value <= self.max_value):
            raise ValidationError(self.message)