import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities before each test."""
    original_activities = copy.deepcopy(app_module.activities)
    app_module.activities.clear()
    app_module.activities.update(original_activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original_activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)


def test_get_activities_returns_seed_data(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_participant(client):
    # Arrange
    new_email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for Chess Club"
    assert new_email in app_module.activities["Chess Club"]["participants"]


def test_signup_for_activity_rejects_duplicate_email(client):
    # Arrange
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
