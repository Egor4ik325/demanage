from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PermissionsConfig(AppConfig):
    """
    Application config for permission administration.
    """

    name = "demanage.permissions"
    verbose_name = _("Permissions")
    label = "permissions"

    def ready(self):
        pass
