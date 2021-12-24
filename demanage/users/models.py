from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from demanage.boards.models import Board


class User(AbstractUser):
    """Default user for Demanage."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def can_view_board(self, board: Board) -> bool:
        """
        Check whether the user is able to view the board.
        """
        if board.organization.representative == self:
            return True

        if board.public and self in board.organization.members:
            return True

        if self.has_perm("view_board", board):
            return True

        return False
