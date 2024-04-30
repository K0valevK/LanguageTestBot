from aiogram import types
from aiogram.utils.formatting import as_list
from database_requests import get_tasks, get_answers
from typing import Dict, List
from utils import safe_request

import random
import text

batch_limit = 10

user_tasks: Dict[int, List] = {}
user_ans: Dict[int, List] = {}
tasks_data: Dict[int, Dict[str, int]] = {}


async def get_new_tasks(user_id: int):
    tasks_data[user_id] = {}
    tasks_data[user_id]["correct"] = 0
    tasks_data[user_id]["question_num"] = 0

    user_tasks[user_id] = await get_tasks(difficulty_min=0.0,
                                          difficulty_max=1.0,
                                          offset=random.randrange(0, 90) * 100,
                                          limit=batch_limit)

    if user_id in user_ans:
        user_ans[user_id].clear()
    else:
        user_ans[user_id] = []

    for task in user_tasks[user_id]:
        user_ans[user_id].append(await get_answers(task.id))


async def next_task(user_id: int):
    ans_text = []
    task_num = tasks_data[user_id]["question_num"]
    batch_num = task_num % batch_limit

    for i in range(len(user_ans[user_id][batch_num])):
        if user_ans[user_id][batch_num][i].is_true:
            tasks_data[user_id]["ans"] = user_ans[user_id][batch_num][i].text

        ans_text.append(user_ans[user_id][batch_num][i].text)
    random.shuffle(ans_text)

    kb = types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text=i) for i in ans_text
        ],
        [types.KeyboardButton(text=text.TEST_QUIT)],
    ], resize_keyboard=True, input_field_placeholder="Ответ")

    task_txt = user_tasks[user_id][batch_num].text.split()
    task_txt[user_ans[user_id][batch_num][0].text_pos] = "*****"
    task_txt = " ".join(task_txt)

    content = as_list(text.QUESTION_NUM.format(task_num + 1),
                      text.QUESTION_TASK,
                      task_txt, sep="\n")

    return content, kb


async def clear_test_data(user_id: int):
    user_tasks.pop(user_id)
    user_ans.pop(user_id)
    tasks_data.pop(user_id)


def get_cur_task_id(user_id: int):
    return user_tasks[user_id][tasks_data[user_id]["question_num"]].id
