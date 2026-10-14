import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.NOTES.clear()
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_version_has_version_and_host(client):
    body = client.get("/version").get_json()
    assert "version" in body
    assert "host" in body


def test_add_and_list_notes(client):
    resp = client.post("/notes", json={"text": "first note"})
    assert resp.status_code == 201
    notes = client.get("/notes").get_json()["notes"]
    assert notes == [{"id": 1, "text": "first note"}]


def test_add_note_without_text_fails(client):
    resp = client.post("/notes", json={})
    assert resp.status_code == 400
