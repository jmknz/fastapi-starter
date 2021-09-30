import pytest

from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestHeartbeat:
    async def test_heartbeat(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for('heartbeat'))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        res_json = res.json()
        assert res_json == {'thump': 'thump'}

