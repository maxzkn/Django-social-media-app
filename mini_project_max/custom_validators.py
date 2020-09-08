from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.utils.translation import gettext as _, ngettext
import re
from difflib import SequenceMatcher


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Slaptažodis per trumpas. Ilgis turi buti ne mažiau %(min_length)d simbolių.",
                    "Slaptažodis per trumpas. Ilgis turi buti ne mažiau %(min_length)d simbolių.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Jūsų slaptažodis turi būti bent %(min_length)d simbolių.",
            "Jūsų slaptažodis turi būti bent %(min_length)d simbolių.",
            self.min_length
        ) % {'min_length': self.min_length}


class CustomUserAttributeSimilarityValidator:
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("Slaptažodis yra per panašus į %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _("Slaptažodis negali būti per daug panašus į asmeninę informaciją.")


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Šis slaptažodis susideda tik iš skaitmenų."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Jūsų slaptažodis negali būti sudėtas tik iš skaitmenų.")