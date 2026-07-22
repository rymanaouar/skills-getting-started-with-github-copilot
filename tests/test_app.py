import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    yield
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


client = TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity():
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Removed michael@mergington.edu from Chess Club"
    )

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_participant_returns_404_for_unknown_activity():
    response = client.delete(
        "/activities/Unknown Activity/participants/michael@mergington.edu"
    )

    assert response.status_code == 404
