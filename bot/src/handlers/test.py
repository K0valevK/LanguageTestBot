from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from database_requests import update_user_leveled_test, update_user_infinite_test
from task_logic import tasks_in_test, tasks_data, endless_tasks_data, clear_endless_test_data
from task_logic import gen_new_test, create_task, clear_test_data
from task_logic import get_new_tasks, next_task
from states import TestingState, LeveledTestState, EndlessTestState
from keyboards import test_kb, difficulty_kb, start_kb

import text
import states

router = Router()


@router.message(Command("test"))
async def command_test(msg: Message, state: FSMContext):
    await state.set_state(TestingState.test_type)
    await msg.answer(text.START_TESTING_MESSAGE, reply_markup=test_kb)


@router.message(TestingState.test_type, F.text.in_(states.available_test_types))
async def select_test_type(msg: Message, state: FSMContext):
    if msg.text.lower() == "по уровню сложности":
        await state.set_state(LeveledTestState.test_difficulty)
        await msg.answer(text.SELECT_DIFF_LEVEL_MESSAGE, reply_markup=difficulty_kb)
    else:
        await state.set_state(EndlessTestState.in_progress)
        await msg.answer(f"Значит {msg.text} уровень? Что ж поехали!", reply_markup=ReplyKeyboardRemove())

        user_id = msg.chat.id

        await get_new_tasks(user_id)
        content, kb = await next_task(user_id)

        await msg.answer(**content.as_kwargs(), reply_markup=kb)


@router.message(LeveledTestState.test_difficulty, F.text.in_(states.available_test_diff))
async def select_difficulty(msg: Message, state: FSMContext):
    await state.set_state(LeveledTestState.in_progress)
    await msg.answer(f"Значит {msg.text} уровень? Что ж поехали!", reply_markup=ReplyKeyboardRemove())

    user_id = msg.chat.id

    await gen_new_test(user_id, msg.text)
    content, kb = await create_task(user_id, 0)

    await msg.answer(**content.as_kwargs(), reply_markup=kb)


@router.message(LeveledTestState.in_progress)
async def task(msg: Message, state: FSMContext):
    user_id = msg.chat.id

    if msg.text == text.TEST_QUIT:
        await finish_test(msg, state)
        return

    if msg.text == tasks_data[user_id]["ans"]:
        tasks_data[user_id]["correct"] += 1
        await msg.answer(text.CONGRATS_MESSAGE, reply_markup=ReplyKeyboardRemove())

    else:
        await msg.answer(text.FAIL_MESSAGE.format(tasks_data[user_id]["ans"]),
                         reply_markup=ReplyKeyboardRemove())

    tasks_data[user_id]["question_num"] += 1

    if tasks_data[user_id]["question_num"] == tasks_in_test:
        await finish_test(msg, state)
        return

    content, kb = await create_task(user_id, tasks_data[user_id]["question_num"])

    await msg.answer(**content.as_kwargs(), reply_markup=kb)


@router.message(EndlessTestState.in_progress)
async def endless_task(msg: Message, state: FSMContext):
    user_id = msg.chat.id

    if msg.text == text.TEST_QUIT:
        await finish_endless(msg, state)
        return

    endless_tasks_data[user_id]["question_num"] += 1
    if msg.text == endless_tasks_data[user_id]["ans"]:
        endless_tasks_data[user_id]["correct"] += 1
        await msg.answer(text.CONGRATS_MESSAGE, reply_markup=ReplyKeyboardRemove())

    else:
        await msg.answer(text.FAIL_MESSAGE.format(endless_tasks_data[user_id]["ans"]),
                         reply_markup=ReplyKeyboardRemove())
        await finish_endless(msg, state)
        return

    if endless_tasks_data[user_id]["question_num"] % 10 == 0:
        await get_new_tasks(user_id)
    content, kb = await next_task(user_id)

    await msg.answer(**content.as_kwargs(), reply_markup=kb)


async def finish_test(msg: Message, state: FSMContext):
    user_id = msg.chat.id
    username = msg.chat.username

    await msg.answer(text.TEST_FINISHED.format(tasks_data[user_id]["correct"],
                                               tasks_data[user_id]["question_num"]),
                     reply_markup=ReplyKeyboardRemove())
    await msg.answer(text.TEST_AFTERSTATE, reply_markup=start_kb)

    await update_user_leveled_test(user_id,
                                   username,
                                   tasks_data[user_id]["correct"],
                                   tasks_data[user_id]["question_num"])
    await clear_test_data(user_id)
    await state.clear()


async def finish_endless(msg: Message, state: FSMContext):
    user_id = msg.chat.id
    username = msg.chat.username

    await msg.answer(text.ENDLESS_FINISHED.format(endless_tasks_data[user_id]["correct"]),
                     reply_markup=start_kb)

    await update_user_infinite_test(user_id,
                                    username,
                                    endless_tasks_data[user_id]["correct"],
                                    endless_tasks_data[user_id]["question_num"],
                                    endless_tasks_data[user_id]["correct"])
    await clear_endless_test_data(user_id)
    await state.clear()
