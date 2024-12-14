import asyncio

from csra_server.db import db_get_tasks
from csra_server.models.task_status import TaskStatus

async def background_task():
    while True:
        tasks = await db_get_tasks()
        queued_tasks = [task for task in tasks if task.status == TaskStatus.QUEUED]
        print(f"Queued tasks are {queued_tasks}")
        await asyncio.sleep(2)