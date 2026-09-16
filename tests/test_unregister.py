"""Tests for DELETE /activities/{activity_name}/signup."""

from src.app import activities


def test_unregister_success_removes_participant(client):
    email = "michael@mergington.edu"  # already registered for Chess Club
    assert email in activities["Chess Club"]["participants"]

    response = client.delete(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Chess Club"
    }
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_activity_not_found(client):
    response = client.delete(
        "/activities/Nonexistent Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_registered(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "not-signed-up@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
