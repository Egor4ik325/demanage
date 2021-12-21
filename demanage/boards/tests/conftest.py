import pytest


@pytest.fixture
def board_data(board_build_dict):
    """Raw data as given by the client."""
    board_data = board_build_dict.copy()
    return board_data


@pytest.fixture
def board_factory():
    """Factory fixture."""
    pass
