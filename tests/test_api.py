from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_process_streams_progress_and_result() -> None:
    with patch("backend.main.asyncio.sleep", new_callable=AsyncMock) as sleep:
        response = client.post("/process", json={"text": "hello"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.headers["cache-control"] == "no-cache"
    assert response.text == "".join(
        f"event: progress\ndata: {percentage}\n\n"
        for percentage in range(0, 101, 10)
    ) + "event: result\ndata: done\n\n"
    assert sleep.await_count == 10
    assert all(call.args == (1,) for call in sleep.await_args_list)


def test_process_rejects_missing_or_non_string_input() -> None:
    for body in ({}, {"text": 123}, {"text": None}):
        assert client.post("/process", json=body).status_code == 422
