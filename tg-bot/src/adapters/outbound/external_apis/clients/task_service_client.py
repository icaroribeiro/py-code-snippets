from typing import Any

from core.ports.outbound.task_port import TaskServiceOutputPort
from infrastructure.config import TaskServiceSettings
from infrastructure.http_client import HTTPClient


class TaskServiceClient(TaskServiceOutputPort):
    def __init__(self, http_client: HTTPClient, settings: TaskServiceSettings) -> None:
        self._http_client = http_client
        self._settings = settings

    async def forward_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self._settings.base_url}/v1/tasks"
        return await self._http_client.post(url, json_data=payload)
