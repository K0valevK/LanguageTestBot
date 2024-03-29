from config import settings

import httpx


async def create_user(telegram_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"http://{settings.database_host}:{settings.database_port}/user",
                                 headers={"accept": "application/json", "Content-Type": "application/json"},
                                 json={"telegram_id": telegram_id, "correct_answers": 0, "tasks_answered": 0})
    return resp


async def get_user(telegram_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://{settings.database_host}:{settings.database_port}/user/{telegram_id}",
                                headers={"accept": "application/json"})
    return resp


async def update_user(telegram_id: int, correct_answers: int, tasks_answered: int):
    async with httpx.AsyncClient() as client:
        resp = await client.put(f"http://{settings.database_host}:{settings.database_port}/user",
                                headers={"accept": "application/json", "Content-Type": "application/json"},
                                json={"telegram_id": telegram_id,
                                      "correct_answers": correct_answers,
                                      "tasks_answered": tasks_answered})
    return resp
