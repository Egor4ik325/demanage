from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BoardsConfig(AppConfig):
    """
    Application config for boards.
    """

    name = "demanage.boards"
    verbose_name = _("Boards")
    label = "boards"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        pass
