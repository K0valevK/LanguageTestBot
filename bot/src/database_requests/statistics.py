import json

from config import settings
from schemas import User

import httpx


base_url = "http://{host}:{port}/user{path}"
post_put_headers = {"accept": "application/json", "Content-Type": "application/json"}
get_headers = {"accept": "application/json"}


def create_url(path, host=settings.database_host, port=settings.database_port):
    return base_url.format(host=host, port=port, path=path)


async def create_user(telegram_id: int, username: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(create_url(""),
                                 headers=post_put_headers,
                                 json={"telegram_id": telegram_id,
                                       "username": username,
                                       "correct_answers": 0,
                                       "tasks_answered": 0,
                                       "max_unlimited_score": 0})
    return resp


async def get_user(telegram_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(create_url(f"/{telegram_id}"),
                                headers=get_headers)
    return resp


async def get_user_name(username: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(create_url(f"/name/{username}"),
                                headers=get_headers)
    return resp


async def update_user_leveled_test(telegram_id: int, username: str, correct_answers: int, tasks_answered: int):
    async with httpx.AsyncClient() as client:
        resp = await client.put(create_url(""),
                                headers=post_put_headers,
                                json={"telegram_id": telegram_id,
                                      "username": username,
                                      "correct_answers": correct_answers,
                                      "tasks_answered": tasks_answered,
                                      "max_unlimited_score": None})
    return resp


async def update_user_infinite_test(telegram_id: int,
                                    username: str,
                                    correct_answers: int,
                                    tasks_answered: int,
                                    max_unlimited_score: int):
    async with httpx.AsyncClient() as client:
        resp = await client.put(create_url(""),
                                headers=post_put_headers,
                                json={"telegram_id": telegram_id,
                                      "username": username,
                                      "correct_answers": correct_answers,
                                      "tasks_answered": tasks_answered,
                                      "max_unlimited_score": max_unlimited_score})
    return resp


async def get_leaders():
    async with httpx.AsyncClient() as client:
        resp = await client.get(create_url("/leaders"),
                                headers=get_headers)
    # TODO finish
    a = json.loads(resp.text)
    return resp
