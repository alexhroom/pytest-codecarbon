import os

import pytest
from codecarbon import EmissionsTracker


class Carbon(object):
    """Adds carbon profiling to your tests."""

    def __init__(self, dir):
        self.dir = dir
        self.tracker = None

    def pytest_sessionstart(self, session):
        """Runs at the start of the test session."""
        try:
            os.mkdir(self.dir)
        except OSError:
            pass

        # instead of instantiating a tracker for each test, we instantiate it once
        # then use find and replace to fill in the names for each test
        self.tracker = EmissionsTracker(
            project_name="#TESTNAME#", output_dir=self.dir, log_level="critical"
        )

    def pytest_sessionfinish(self, session):
        """Runs at the end of the test session."""
        pass

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        """Hook wrapper around each Pytest test."""
        self.tracker.start()
        yield
        self.tracker.stop()
        with open(f"{self.dir}/emissions.csv", "r", encoding="utf-8") as file:
            data = file.read()
            data = data.replace("#TESTNAME#", item.name)

        with open(f"{self.dir}/emissions.csv", "w", encoding="utf-8") as file:
            file.write(data)


def pytest_addoption(parser):
    """Pytest option hook for pytest-codecarbon"""
    group = parser.getgroup("Carbon")
    group.addoption("--carbon", action="store_true", help="generate carbon information")
    group.addoption(
        "--carbon-dir",
        default=f"{os.getcwd()}",
        help="directory for pytest-codecarbon result files",
    )


def pytest_configure(config):
    """Pytest config hook for pytest-codecarbon"""
    if config.getvalue("carbon"):
        config.pluginmanager.register(Carbon(config.getvalue("carbon_dir")))
