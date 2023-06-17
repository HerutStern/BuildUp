from django.core.exceptions import ValidationError


def validate_delete(val):
    if type(val) is not bool:
        raise ValidationError("Delete column did not get a Boolean type of value")