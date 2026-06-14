from typing import Optional

from adapters.outbound.persistence.mongodb.task.documents import (
    TaskDocument,
)
from adapters.outbound.persistence.mongodb.task.mapper import (
    TaskMapper,
)
from core.domain.task import Task
from core.ports.outbound.task_port import (
    TaskRepositoryOutputPort,
)


class MongoDBTaskRepository(TaskRepositoryOutputPort):
    def __init__(self) -> None:
        pass

    async def save(self, task: Task) -> Task:
        document = TaskMapper.to_document(task)
        await document.save()
        return TaskMapper.to_domain(document)

    async def find_by_id(self, task_id: str) -> Optional[Task]:
        document = await TaskDocument.get(task_id)
        if not document:
            return None
        return TaskMapper.to_domain(document)
