"""
Defining pytest session details

"""
import os
import sys
import pytest
import utils.delete_test_log_files as delete
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def pytest_sessionstart(session):
    """
    pytest session start
    """
    session.results = dict()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Running wrapper method
    """
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result

def pytest_sessionfinish(session):
    """
    pytest session finish
    """
    failed_amount = sum(1 for result in session.results.values() if result.failed)
    if failed_amount == 0:
        print(f'\n{failed_amount} failure results')
        delete.delete_pickle_file()
        delete.delete_pact_json_file()
