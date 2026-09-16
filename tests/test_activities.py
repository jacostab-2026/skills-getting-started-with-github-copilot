"""Tests for the root redirect and the GET /activities endpoint."""

from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    body = response.json()
    assert body == activities
    assert "Chess Club" in body


def test_get_activities_includes_expected_fields(client):
    response = client.get("/activities")

    body = response.json()
    chess_club = body["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)
