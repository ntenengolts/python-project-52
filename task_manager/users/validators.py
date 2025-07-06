from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomMinimumLengthValidator:
    def __init__(self, min_length=3):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f"Ваш пароль должен содержать как минимум "
                  f"{self.min_length} символа."),
                code="password_too_short",
            )

    def get_help_text(self):
        return _(f"Ваш пароль должен содержать как минимум "
                 f"{self.min_length} символа.")
