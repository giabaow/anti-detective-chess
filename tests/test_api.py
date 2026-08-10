from fastapi.testclient import TestClient

from anti_cheat_detective.api.app import app

client = TestClient(app)


def test_index_serves_analysis_interface() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Anti-cheat Detective" in response.text
    assert 'id="analysis-form"' in response.text


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_rejects_invalid_pgn_before_queueing() -> None:
    response = client.post("/v1/analyses", json={"pgn": "not a game"})

    assert response.status_code == 422


def test_missing_job_returns_not_found() -> None:
    response = client.get("/v1/analyses/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
