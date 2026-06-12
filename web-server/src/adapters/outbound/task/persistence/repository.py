from typing import Optional

from adapters.outbound.task.persistence.documents import (
    TaskDocument,
)
from adapters.outbound.task.persistence.mapper import (
    TaskMapper,
)
from core.domain.task import Task
from core.ports.outbound.task.persistence.repository_output_port import (
    TaskRepositoryOutputPort,
)


class TaskRepository(TaskRepositoryOutputPort):
    async def save(self, task: Task) -> Task:
        document = TaskMapper.to_document(task)
        await document.save()
        return TaskMapper.to_domain(document)

    async def find_by_id(self, task_id: str) -> Optional[Task]:
        document = await TaskDocument.get(task_id)
        if not document:
            return None
        return TaskMapper.to_domain(document)

    async def find_latest_by_user(self, user_id: str) -> Optional[Task]:
        document = await TaskDocument.find_one(
            {"user_id": user_id},
            sort="-created_at",
        )
        if not document:
            return None
        return TaskMapper.to_domain(document)
