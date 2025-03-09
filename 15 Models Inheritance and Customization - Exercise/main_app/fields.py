from django.db import models
from django.core.exceptions import ValidationError


class StudentIDField(models.PositiveIntegerField):

    @staticmethod
    def parse_value(value):
        try:
            return int(value)
        except ValueError:
            raise ValueError("Invalid input for student ID")

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    def to_python(self, value):
        return self.parse_value(value)

    def get_prep_value(self, value):
        value = self.parse_value(value)

        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")
        return value

class AnimalIDField(models.PositiveIntegerField):

    @staticmethod
    def parse_into_int(value):
        try:
            return int(value)
        except ValueError:
            raise ValueError("Invalid input for animal ID")

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return value
        return self.parse_into_int(value)

    def get_prep_value(self, value):
        value = self.parse_into_int(value)

        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")
        return value


class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return f"****-****-****-{value[-4:]}"


class MaskedEmployeeIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        super().__init__(*args, **kwargs)
    #
    # def from_db_value(self, value, expression, connection):
    #     if value is None:
    #         return value
    #     return self.to_python(value)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The employee ID must be a string")
        if not value.isdigit():
            raise ValidationError("The employee ID must contain only digits")
        if len(value) != 10:
            raise ValidationError("The employee ID must be exactly 10 characters long")

        return f'*******{value[-3:]}'


















































