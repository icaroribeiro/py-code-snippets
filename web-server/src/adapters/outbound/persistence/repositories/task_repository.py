from typing import Optional

from adapters.outbound.persistence.documents.task_document import (
    TaskDocument,
)
from adapters.outbound.persistence.mappers.task_mapper import (
    TaskMapper,
)
from core.domain.task import Task
from core.ports.outbound.persistence.task_repository_port import (
    TaskRepositoryPort,
)


class TaskRepository(TaskRepositoryPort):
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
