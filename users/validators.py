import re
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User


from django.contrib import messages

SALT = 'DLZjTiZxI1OE6pfFd9xVZwaaINK34JTF6BQdzb6bAPFFgUDgBneNiBwq6Oxs1upwe3MEr5R13pt3QFEbsuaPHDTroxsEGlIDyPBRhJd6jJTMg'

class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            return True
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_no_number',
            )
            return True

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            return True
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            return True
            raise ValidationError(
                _("The password must contain at least 1 special character: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 special character: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )


class LengthValidator(object):
    def validate(self, password, user=None):
        if len(password)<9:
            return True
            raise ValidationError(
                _("The password must contain at least 1 special character: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 special character: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )
class RepeatedValidator(object):
    def validate(self, password, user=None):
        # In case there is no user this validator is not applicable, so we return success
        if user is None:
            return None

        hashed_password = make_password(password, salt=SALT)
        saved_password = User.objects.filter(user=user, password=hashed_password).first()
        if saved_password is not None:
            return True
            raise ValidationError(
                _("The password cannot be the same as previously used passwords."),
                code='password_no_symbol',
            )

    def password_changed(self, password, user=None):
        # In case there is no user this is not applicable
        if user is None:
            return None

        hashed_password = make_password(password, salt=SALT)
        saved_password = User.objects.filter(user=user, password=hashed_password).first()
        if saved_password is None:
            saved_password = User()
            saved_password.user = user
            saved_password.password = hashed_password
            saved_password.save()

    def get_help_text(self):
        return _(
            "Your password cannot be the same as previously used passwords."
        )