"""Tests the results output from test_mocks.py"""

import pandas as pd

dataframe = pd.read_csv("emissions.csv")


def test_correct_size():
    """Tests that the size of the dataframe is the correct length."""
    assert dataframe.shape[0] == 4


def test_correct_tests():
    """Tests that the test names have been correctly put into the table."""
    tests = [
        "test_mock_1",
        "test_mock_parametrize[0.01]",
        "test_mock_parametrize[0.03]",
        "test_mock_parametrize[0.04]",
    ]

    assert list(dataframe["project_name"]) == tests
