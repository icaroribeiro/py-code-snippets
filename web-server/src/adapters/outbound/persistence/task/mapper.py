from adapters.outbound.persistence.task.documents import (
    TaskDocument,
)
from core.domain.task import Task, TaskStatus


class TaskMapper:
    @staticmethod
    def to_domain(doc: TaskDocument) -> Task:
        data = doc.model_dump()
        return Task(
            id=str(doc.id),
            status=TaskStatus(data["status"]),
            user_id=data.get("user_id"),
            payload=data.get("payload", {}),
            metadata=data.get("metadata", {}),
            result=data.get("result"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    @staticmethod
    def to_document(domain: Task) -> TaskDocument:
        document_data = {
            "status": domain.status.value,
            "user_id": domain.user_id,
            "payload": domain.payload,
            "metadata": domain.metadata,
            "result": domain.result,
            "created_at": domain.created_at,
            "updated_at": domain.updated_at,
        }
        return TaskDocument(**document_data)
