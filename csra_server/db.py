from datetime import datetime
from typing import List

import aiosqlite

from csra_server.models.task import Task
from csra_server.models.task_status import TaskStatus

DB_URL = "csra.db"


async def create_db_if_not_exists() -> None:
    async with aiosqlite.connect(DB_URL) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_string TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL CHECK (status in ('QUEUED', 'RUNNING', 'COMPLETED', 'FAILED')) DEFAULT 'QUEUED'
        )
        """)
        await db.commit()


async def db_get_tasks() -> List[Task]:
    async with aiosqlite.connect(DB_URL) as db:
        async with db.execute("SELECT * FROM tasks") as cursor:
            rows = await cursor.fetchall()
            tasks = [
                Task(
                    query_string=row[1],
                    created_on=datetime.fromisoformat(row[2]),
                    status=TaskStatus(row[3])
                )
                for row in rows
            ]
        return tasks


async def db_create_task(task: Task) -> None:
    async with aiosqlite.connect(DB_URL) as db:
        await db.execute(f"INSERT INTO tasks VALUES ({task.query_string})")
        await db.commit()