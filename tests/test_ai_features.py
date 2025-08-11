import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ai_action_items_endpoint_success(monkeypatch):
    # Mock the generator to avoid real OpenAI calls
    def fake_generate_action_items(description: str):
        assert "roadmap" in description
        return [
            "Draft Q3 roadmap",
            "Assign onboarding owners",
            "Prepare weekly KPI dashboard",
        ]

    # Patch where it's used
    import app.routers.notes as notes_router

    monkeypatch.setattr(notes_router, "generate_action_items", fake_generate_action_items)

    resp = client.post(
        "/notes/ai-action-items",
        params={"description": "Discuss Q3 roadmap, onboarding owners, KPI dashboard."},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0].startswith("Draft Q3")


def test_ai_action_items_endpoint_missing_description():
    resp = client.post("/notes/ai-action-items")
    assert resp.status_code == 400
    body = resp.json()
    assert body["detail"] == "Description is required"


def test_ai_action_items_endpoint_upstream_error(monkeypatch):
    def raising_generate_action_items(description: str):
        raise RuntimeError("OpenAI failure")

    import app.routers.notes as notes_router

    monkeypatch.setattr(notes_router, "generate_action_items", raising_generate_action_items)

    resp = client.post(
        "/notes/ai-action-items",
        params={"description": "something"},
    )
    assert resp.status_code == 502
    assert resp.json()["detail"] == "Failed to generate action items"


def test_create_note_auto_generates_action_items_when_missing(monkeypatch):
    def fake_generate_action_items(description: str):
        return ["Item A", "Item B"]

    import app.routers.notes as notes_router

    monkeypatch.setattr(notes_router, "generate_action_items", fake_generate_action_items)

    payload = {
        "title": "Team Sync",
        "description": "Plan next sprint and assign tasks",
        "status": "open",
        "date": "2024-01-01T00:00:00Z",
        # action_items intentionally omitted
    }
    resp = client.post("/notes/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["action_items"] == ["Item A", "Item B"]


def test_create_note_ai_failure_falls_back_to_empty(monkeypatch):
    def raising_generate_action_items(description: str):
        raise RuntimeError("OpenAI failure")

    import app.routers.notes as notes_router

    monkeypatch.setattr(notes_router, "generate_action_items", raising_generate_action_items)

    payload = {
        "title": "Team Sync",
        "description": "Plan next sprint and assign tasks",
        "status": "open",
        "date": "2024-01-01T00:00:00Z",
        # action_items intentionally omitted
    }
    resp = client.post("/notes/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["action_items"] == []
