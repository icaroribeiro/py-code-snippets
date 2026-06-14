import httpx
from typing import Any

from infrastructure.config import HTTPClientSettings
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)

class HTTPServer:
    def __init__(self, settings: HTTPClientSettings) -> None:
        self._settings = settings
        self._client: httpx.AsyncClient | None = None

    def start(self) -> None:
        if not self._client:
            self._client = httpx.AsyncClient(timeout=httpx.Timeout(self._settings.timeout_seconds))

    async def stop(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def post(self, url: str, json_data: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
        if not self._client:
            raise RuntimeError("HTTPClient network session layer is not running.")

        response = await self._client.post(url, json=json_data, headers=headers)
        response.raise_for_status()
        return response.json()
