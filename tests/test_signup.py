"""Tests for POST /activities/{activity_name}/signup."""

from src.app import activities


def test_signup_success_adds_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Chess Club"
    }
    assert email in activities["Chess Club"]["participants"]


def test_signup_activity_not_found(client):
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_rejected(client):
    email = "michael@mergington.edu"  # already registered for Chess Club

    response = client.post(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"
    # Participant list should not contain a duplicate entry.
    assert activities["Chess Club"]["participants"].count(email) == 1
