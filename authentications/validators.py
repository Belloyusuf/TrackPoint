from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

# password can be `1234` else will raise Validation error 

class AllowSimplePasswordValidator:
    """ avoid using it in production  """
    def validate(self, password, user=None):
        if password == '1234':
            return
        raise ValidationError(
            _("This password is too simple."),
            code='password_too_simple',
        )

    def get_help_text(self):
        return _("Your password can be '1234' for testing.")
