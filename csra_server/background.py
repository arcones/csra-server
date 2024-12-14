import asyncio

from csra_server.db import db_get_tasks, db_update_task_status
from csra_server.models.task import Task
from csra_server.models.task_status import TaskStatus


async def process_task(task):
    await asyncio.sleep(2) # TODO Actually process the task
    await db_update_task_status(task, TaskStatus.COMPLETED)
    print(f"Task with ID {task.id} completed")

async def background_task():
    semaphore = asyncio.Semaphore(3)
    active_tasks = set()

    async def run_task_with_semaphore(task: Task):
        async with semaphore:
            await process_task(task)
        active_tasks.remove(task)

    while True:
        tasks = await db_get_tasks()
        queued_tasks = [task for task in tasks if task.status == TaskStatus.QUEUED]
        print(f"Queued tasks are {queued_tasks}")
        for queued_task in queued_tasks:
            if queued_task not in active_tasks:
                active_tasks.add(queued_task)
                asyncio.create_task(run_task_with_semaphore(queued_task))

        await asyncio.sleep(2)