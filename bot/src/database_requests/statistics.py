import json

from config import settings
from schemas import User, Statistics

import httpx

user_url = "http://{host}:{port}/user{path}"
statistics_url = "http://{host}:{port}/statistics{path}"
post_put_headers = {"accept": "application/json", "Content-Type": "application/json"}
get_headers = {"accept": "application/json"}


def create_user_url(path, host=settings.database_host, port=settings.database_port):
    return user_url.format(host=host, port=port, path=path)


def create_statistics_url(path, host=settings.database_host, port=settings.database_port):
    return statistics_url.format(host=host, port=port, path=path)


async def create_user(telegram_id: int, username: str):
    async with httpx.AsyncClient() as client:
        resp_user = await client.post(create_user_url(""),
                                      headers=post_put_headers,
                                      json={"telegram_id": telegram_id,
                                            "username": username})
        tmp = json.loads(resp_user.text)["id"]
        resp_stats = await client.post(create_statistics_url(""),
                                       headers=post_put_headers,
                                       json={"user_id": json.loads(resp_user.text)["id"],
                                             "correct_answers": 0,
                                             "tasks_answered": 0,
                                             "max_unlimited_score": 0})

    return resp_user


async def get_user(telegram_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(create_user_url(f"/{telegram_id}"),
                                headers=get_headers)
    return resp


async def get_user_by_id(id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(create_user_url(f"/id/{id}"),
                                headers=get_headers)
    return resp


async def get_user_name(username: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(create_user_url(f"/name/{username}"),
                                headers=get_headers)
    return resp


async def get_stats_by_uid(user_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(create_statistics_url(f"/{user_id}"),
                                headers=get_headers)

    return resp


async def update_user_leveled_test(telegram_id: int, username: str, correct_answers: int, tasks_answered: int):
    resp = await get_user(telegram_id)

    async with httpx.AsyncClient() as client:
        await client.put(create_user_url(""),
                         headers=post_put_headers,
                         json={"telegram_id": telegram_id,
                               "username": username})

        resp = await client.put(create_statistics_url(""),
                                headers=post_put_headers,
                                json={"user_id": json.loads(resp.text)["id"],
                                      "correct_answers": correct_answers,
                                      "tasks_answered": tasks_answered,
                                      "max_unlimited_score": None})
    return resp


async def update_user_infinite_test(telegram_id: int,
                                    username: str,
                                    correct_answers: int,
                                    tasks_answered: int,
                                    max_unlimited_score: int):
    resp = await get_user(telegram_id)

    async with httpx.AsyncClient() as client:
        await client.put(create_user_url(""),
                         headers=post_put_headers,
                         json={"telegram_id": telegram_id,
                               "username": username})

        resp = await client.put(create_statistics_url(""),
                                headers=post_put_headers,
                                json={"user_id": json.loads(resp.text)["id"],
                                      "correct_answers": correct_answers,
                                      "tasks_answered": tasks_answered,
                                      "max_unlimited_score": max_unlimited_score})
    return resp


async def get_leaders():
    async with httpx.AsyncClient() as client:
        resp = await client.get(create_statistics_url("/leaders/tasks"),
                                headers=get_headers)
        leaders_tasks_stats = [Statistics(**i) for i in json.loads(resp.text)]
        leader_tasks_users = []
        for i in leaders_tasks_stats:
            leader_tasks_users.append(User(**(json.loads((await get_user_by_id(i.user_id)).text))))
        leaders_tasks = list(zip(leaders_tasks_stats, leader_tasks_users))

        resp = await client.get(create_statistics_url("/leaders/endless"),
                                headers=get_headers)
        leaders_endless_stats = [Statistics(**i) for i in json.loads(resp.text)]
        leaders_endless_users = []
        for i in leaders_endless_stats:
            leaders_endless_users.append(User(**(json.loads((await get_user_by_id(i.user_id)).text))))
        leaders_endless = list(zip(leaders_endless_stats, leaders_endless_users))

    return {"endless": leaders_endless, "tasks": leaders_tasks}
