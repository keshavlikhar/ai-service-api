from fastapi.testclient import TestClient

from ai_service_api.main import app

client = TestClient(app)


def test_inspect_prompt() -> None:
    response = client.post(
        "/v1/prompts/inspect",
        json={"prompt": "Build reliable AI services"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "character_count": 26,
        "word_count": 4,
    }


def test_inspect_prompt_rejects_empty_prompt() -> None:
    response = client.post(
        "/v1/prompts/inspect",
        json={"prompt": ""},
    )

    assert response.status_code == 422
