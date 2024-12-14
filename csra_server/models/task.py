from datetime import datetime
from pydantic import BaseModel
from csra_server.models.task_status import TaskStatus

class Task(BaseModel):
    id: int = None
    query_string: str
    created_on: datetime = datetime.now()
    status: TaskStatus = TaskStatus.QUEUED

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id