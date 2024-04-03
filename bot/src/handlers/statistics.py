from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from database_requests import get_user, get_user_name, get_leaders
from states import StatisticsState
from keyboards import statistics_kb, start_kb
from logs import log, get_current_time, get_stats_key

import json
import text
import states

router = Router()


@router.message(Command("statistics"))
async def command_statistics(msg: Message, state: FSMContext):
    log("user_journey", timestamp=get_current_time(), user_id=msg.from_user.id,
        event_group="click2button", event_name="statistics", event_data="None")

    await state.set_state(StatisticsState.statistics_type)
    await msg.answer(text.START_STATS_MESSAGE, reply_markup=statistics_kb)


@router.message(StatisticsState.statistics_type, F.text.in_(states.available_statistics_types))
async def select_statistics_type(msg: Message, state: FSMContext):
    log("user_journey", timestamp=get_current_time(), user_id=msg.from_user.id,
        event_group="click2button", event_name="statistics_get_type", event_data=get_stats_key(msg.text))

    if msg.text.lower() == "моя":
        user = json.loads((await get_user(msg.from_user.id)).text)
        await msg.answer(text.RESULTS.format(user['correct_answers'],
                                             user['correct_answers'] / user['tasks_answered'],
                                             user['max_unlimited_score']),
                         reply_markup=start_kb)
    elif msg.text.lower() == "найти по username":
        await state.clear()
        await state.set_state(StatisticsState.seek_by_username)
        await msg.answer(text.FIND_BY_USERNAME, reply_markup=ReplyKeyboardRemove())
        return

    elif msg.text.lower() == "лидеры":
        users = await get_leaders()
        # TODO finish

    await state.clear()


@router.message(StatisticsState.seek_by_username)
async def find_by_username(msg: Message, state: FSMContext):
    log("user_journey", timestamp=get_current_time(), user_id=msg.from_user.id,
        event_group="kb_enter", event_name="statistics_get_by_name", event_data=msg.text)

    user = json.loads((await get_user_name(msg.text)).text)
    await msg.answer(text.RESULTS_ELSE.format(user['username'],
                                              user['correct_answers'],
                                              user['correct_answers'] / user['tasks_answered'],
                                              user['max_unlimited_score']),
                     reply_markup=start_kb)
    await state.clear()
