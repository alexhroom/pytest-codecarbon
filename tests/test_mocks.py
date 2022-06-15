"""Mock tests used to test that everything works"""

import pytest

from time import sleep


def test_mock_1():
    sleep(0.01)


@pytest.mark.parametrize("time", [0.01, 0.03, 0.04])
def test_mock_parametrize(time):
    sleep(time)
