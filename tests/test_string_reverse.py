import pytest

from test_rig_control_model.module import reverse_string

test_strings = [("hello", "olleh"), ("racecar", "racecar"), ("Racecar", "racecaR")]


@pytest.mark.parametrize("test_string, expected", test_strings)
def test_reverse_string(test_string, expected):
    reversed_string = reverse_string(test_string)
    assert reversed_string == expected
