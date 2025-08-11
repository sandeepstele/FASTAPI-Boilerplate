from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_note():
    payload = {
        "title": "Test Note",
        "description": "A note for testing",
        "status": "open",
        "date": "2024-01-01T00:00:00Z",
        "action_items": ["item1", "item2"],
    }
    response = client.post("/notes/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["action_items"] == payload["action_items"]


def test_read_notes():
    client.post(
        "/notes/",
        json={
            "title": "Another Note",
            "description": "desc",
            "status": "open",
            "date": "2024-01-02T00:00:00Z",
            "action_items": [],
        },
    )
    response = client.get("/notes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_note():
    create = client.post(
        "/notes/",
        json={
            "title": "Old Title",
            "description": "desc",
            "status": "open",
            "date": "2024-01-03T00:00:00Z",
            "action_items": [],
        },
    )
    note_id = create.json()["id"]
    response = client.put(f"/notes/{note_id}", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_delete_note():
    create = client.post(
        "/notes/",
        json={
            "title": "Delete Me",
            "description": "desc",
            "status": "open",
            "date": "2024-01-04T00:00:00Z",
            "action_items": [],
        },
    )
    note_id = create.json()["id"]
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Note deleted"
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404
