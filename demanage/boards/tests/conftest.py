import pytest

from demanage.conftest import board


@pytest.fixture
def board_data(board_build_dict):
    """Raw data as given by the client."""
    board_data = board_build_dict.copy()
    return board_data
