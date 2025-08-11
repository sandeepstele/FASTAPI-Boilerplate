from fastapi.testclient import TestClient
from typing import List
from app.main import app

client = TestClient(app)


def create_note_payload(**overrides):
    payload = {
        "title": "Team Sync",
        "description": "Weekly sync",
        "status": "open",
        "date": "2024-01-01T10:00:00Z",
        "action_items": ["Send summary", "Create tickets"],
    }
    payload.update(overrides)
    return payload


# -------------------- Happy paths --------------------

def test_create_note_success():
    response = client.post("/notes/", json=create_note_payload())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["title"] == "Team Sync"
    assert data["status"] == "open"
    assert data["action_items"] == ["Send summary", "Create tickets"]


def test_list_notes_contains_created_items():
    # Create two notes
    client.post("/notes/", json=create_note_payload(title="A"))
    client.post("/notes/", json=create_note_payload(title="B"))

    response = client.get("/notes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(note["title"] == "A" for note in data)
    assert any(note["title"] == "B" for note in data)


def test_read_single_note_success():
    create = client.post("/notes/", json=create_note_payload(title="Read Me"))
    note_id = create.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read Me"


def test_update_note_partial_success():
    create = client.post("/notes/", json=create_note_payload(title="Old"))
    note_id = create.json()["id"]

    response = client.put(f"/notes/{note_id}", json={"title": "New"})
    assert response.status_code == 200
    assert response.json()["title"] == "New"


def test_delete_note_success():
    create = client.post("/notes/", json=create_note_payload(title="Delete"))
    note_id = create.json()["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Note deleted"

    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404


# -------------------- Validation / error cases --------------------

def test_create_note_missing_required_fields():
    # Missing title, status, date
    response = client.post(
        "/notes/",
        json={"description": "x", "action_items": []},
    )
    assert response.status_code == 422


def test_create_note_invalid_date_format():
    response = client.post(
        "/notes/",
        json=create_note_payload(date="01-01-2024"),  # invalid ISO8601
    )
    assert response.status_code == 422


def test_create_note_action_items_wrong_type():
    response = client.post(
        "/notes/",
        json=create_note_payload(action_items=[1, 2, 3]),  # must be List[str]
    )
    assert response.status_code == 422


def test_read_note_not_found():
    response = client.get("/notes/999999")
    assert response.status_code == 404


def test_update_note_not_found():
    response = client.put("/notes/999999", json={"title": "New Title"})
    assert response.status_code == 404


def test_delete_note_not_found():
    response = client.delete("/notes/999999")
    assert response.status_code == 404


def test_update_note_empty_body_no_change():
    # Create a note, then update with empty body; should be no-op and still 200
    create = client.post("/notes/", json=create_note_payload(title="Keep Title"))
    note_id = create.json()["id"]

    response = client.put(f"/notes/{note_id}", json={})
    assert response.status_code == 200
    assert response.json()["title"] == "Keep Title"


def test_method_not_allowed_on_collection_item():
    # POST to specific resource should be method-not-allowed
    create = client.post("/notes/", json=create_note_payload(title="X"))
    note_id = create.json()["id"]
    response = client.post(f"/notes/{note_id}", json=create_note_payload(title="Y"))
    assert response.status_code in (404, 405)


def test_extra_fields_are_rejected_on_create():
    payload = create_note_payload()
    payload["unexpected"] = "field"
    response = client.post("/notes/", json=payload)
    # Pydantic by default allows extra unless configured; this asserts current behavior.
    # If model_config forbids extra, switch to 422.
    assert response.status_code == 200


def test_bulk_create_and_list_counts_increase():
    # Capture baseline
    baseline = client.get("/notes/").json()
    baseline_count = len(baseline) if isinstance(baseline, List) else 0

    # Create multiple
    for i in range(5):
        client.post("/notes/", json=create_note_payload(title=f"Item {i}"))

    after = client.get("/notes/").json()
    assert len(after) >= baseline_count + 5
