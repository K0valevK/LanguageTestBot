from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from database_requests import get_user, create_user, update_user
from database_requests import get_tasks, get_answers

from states import TestingState, LeveledTestState
from keyboards import test_kb, difficulty_kb

import json
import text
import states

from task_logic import level_range, batch_limit, tasks_in_test

router = Router()

old_correct_ans = 0
old_tasks_ans = 0
correct_ans_cnt = 0
ans_cnt = 0

task_counter = 1
tasks = []
answers = []


@router.message(Command("test"))
async def command_test(msg: Message, state: FSMContext):
    global old_correct_ans, old_tasks_ans

    await state.set_state(TestingState.test_type)
    await msg.answer(text.START_TESTING_MESSAGE, reply_markup=test_kb)
    user = json.loads((await get_user(msg.from_user.id)).text)
    old_correct_ans, old_tasks_ans = user['correct_answers'], user['tasks_answered']


@router.message(TestingState.test_type, F.text.in_(states.available_test_types))
async def select_test_type(msg: Message, state: FSMContext):
    if msg.text.lower() == "по уровню сложности":
        await state.set_state(LeveledTestState.test_difficulty)
        await msg.answer(text.SELECT_DIFF_LEVEL_MESSAGE, reply_markup=difficulty_kb)
    else:
        await msg.answer('LMAO GOT EM')


@router.message(LeveledTestState.test_difficulty, F.text.in_(states.available_test_diff))
async def select_difficulty(msg: Message, state: FSMContext):
    global task_counter, tasks, answers

    await state.set_state(LeveledTestState.in_progress)
    await msg.answer(f"Значит {msg.text} уровень? Что ж поехали!", reply_markup=ReplyKeyboardRemove())

    params = level_range[msg.text]
    tasks = await get_tasks(**params, limit=batch_limit)
    answers.clear()
    for i in range(10):
        answers.append(await get_answers(tasks[i].id))

    kb = types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text=i.text) for i in answers[0]
        ],
    ], resize_keyboard=True, input_field_placeholder="Ответ")

    await msg.answer(tasks[0].text, reply_markup=kb)


@router.message(LeveledTestState.in_progress)
async def task(msg: Message, state: FSMContext):
    global task_counter, tasks, answers

    print('l')

    if task_counter == tasks_in_test:
        await state.clear()
