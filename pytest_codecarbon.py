import os
import contextlib

import pytest
from codecarbon import EmissionsTracker

class Carbon(object):
    """Adds carbon profiling to your tests."""
    
    def __init__(self, dir):
        self.dir = dir
        self.tracker = None
        
    def pytest_sessionstart(self, session):
        try:
            os.mkdir(self.dir)
        except OSError:
            pass
        
    def pytest_sessionfinish(self, session):
        pass

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        tracker = EmissionsTracker(project_name=item.name, output_dir=self.dir, log_level='critical')
        tracker.start()
        yield
        tracker.stop()


def pytest_addoption(parser):
    """Pytest option hook for pytest-codecarbon"""
    group = parser.getgroup("Carbon")
    group.addoption('--carbon', action='store_true', help="generate carbon information")
    group.addoption('--carbon-dir', default=f"{os.getcwd()}", help="directory for pytest-codecarbon result files")
    
def pytest_configure(config):
    """Pytest config hook for pytest-codecarbon"""
    if config.getvalue('carbon'):
        config.pluginmanager.register(Carbon(config.getvalue('carbon_dir')))
