import asyncio
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI

from csra_server.background import background_task
from csra_server.db import create_db_if_not_exists, db_get_tasks, db_create_task
from csra_server.models.task import Task


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await create_db_if_not_exists()
    background_task_instance = asyncio.create_task(background_task())
    yield
    background_task_instance.cancel()
    try:
        await background_task_instance
    except asyncio.CancelledError:
        print("Background task cancelled.")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to CSRA Server. Use the CLI to interact with the server."}


@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return await db_get_tasks()


@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    await db_create_task(task)
    return task
