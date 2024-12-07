from datetime import datetime
from pydantic import BaseModel
from csra_server.models.task_status import TaskStatus

class Task(BaseModel):
    query_string: str
    created_on: datetime = datetime.now()
    status: TaskStatus = TaskStatus.QUEUED
