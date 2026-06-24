from typing import Any

from core.ports.outbound import TaskServiceApiOutputPort
from infrastructure.config import TaskServiceApiSettings
from infrastructure.http_client import HTTPClient


class TaskServiceApi(TaskServiceApiOutputPort):
    def __init__(
        self, http_client: HTTPClient, settings: TaskServiceApiSettings
    ) -> None:
        self._http_client = http_client
        self._settings = settings

    async def forward_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self._settings.base_url}/v1/tasks"
        return await self._http_client.post(url, json_data=payload)
