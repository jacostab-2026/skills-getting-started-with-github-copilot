"""Shared pytest fixtures for the Mergington High School API tests."""

import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

# Snapshot of the in-memory activities database taken at import time, before
# any test mutates it. Used to reset state between tests.
_INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """A FastAPI TestClient for issuing requests against the app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` store before and after each test.

    `activities` is a module-level dict shared across requests, so tests that
    sign up or unregister participants would otherwise leak state into later
    tests.
    """
    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
