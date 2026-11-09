import os
import pytest
from ghost_sentry.core import GhostSentry

TEST_STATE_FILE = "test_sentry_state.json"

@pytest.fixture(autouse=True)
def cleanup_state():
    if os.path.exists(TEST_STATE_FILE):
        os.remove(TEST_STATE_FILE)
    yield
    if os.path.exists(TEST_STATE_FILE):
        os.remove(TEST_STATE_FILE)

def test_authorization_within_budget():
    sentry = GhostSentry(budget_limit=10.0, persistence_file=TEST_STATE_FILE)
    assert sentry.authorize_request(3.5) is True
    assert sentry.current_spend == 3.5
    assert sentry.is_open is False

def test_circuit_breaker_trips_when_budget_exceeded():
    sentry = GhostSentry(budget_limit=10.0, persistence_file=TEST_STATE_FILE)
    assert sentry.authorize_request(3.5) is True
    assert sentry.authorize_request(8.0) is False
    assert sentry.is_open is True
    assert sentry.current_spend == 3.5

def test_subsequent_requests_blocked_when_open():
    sentry = GhostSentry(budget_limit=5.0, persistence_file=TEST_STATE_FILE)
    assert sentry.authorize_request(6.0) is False
    assert sentry.is_open is True
    assert sentry.authorize_request(1.0) is False
