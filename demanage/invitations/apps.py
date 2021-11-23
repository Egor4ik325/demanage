from django.apps import AppConfig


class InvitationsConfig(AppConfig):
    """
    Application config for invitations.
    """

    name = "demanage.invitations"
    label = "invitations"
    verbose_name = "_(Invitations)"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        pass
