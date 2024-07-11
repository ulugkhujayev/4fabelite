from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordCharacterValidator:
    def __init__(
        self,
        min_length_digit=1,
        min_length_alpha=1,
        min_length_special=1,
        min_length_lower=1,
        min_length_upper=1,
    ):
        self.min_length_digit = min_length_digit
        self.min_length_alpha = min_length_alpha
        self.min_length_special = min_length_special
        self.min_length_lower = min_length_lower
        self.min_length_upper = min_length_upper

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы %(min_length)d цифру.")
                % {"min_length": self.min_length_digit}
            )
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы %(min_length)d букву.")
                % {"min_length": self.min_length_alpha}
            )
        if not any(not char.isalnum() for char in password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы %(min_length)d специальный символ.")
                % {"min_length": self.min_length_special}
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы %(min_length)d строчную букву.")
                % {"min_length": self.min_length_lower}
            )
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы %(min_length)d заглавную букву.")
                % {"min_length": self.min_length_upper}
            )
