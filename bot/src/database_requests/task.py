from config import settings
from schemas import Task, Answer
from typing import List

import httpx
import json


async def get_tasks(difficulty_min: float, difficulty_max: float, offset: int, limit: int) -> List[Task]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://{settings.database_host}:{settings.database_port}/task",
                                headers={"accept": "application/json"},
                                params={"difficulty_min": difficulty_min,
                                        "difficulty_max": difficulty_max,
                                        "offset": offset,
                                        "limit": limit})
    return [Task(**i) for i in json.loads(resp.text)]


async def get_answers(task_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://{settings.database_host}:{settings.database_port}/task/ans/{task_id}",
                                headers={"accept": "application/json"})
    return [Answer(**i) for i in json.loads(resp.text)]
