from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.formatting import as_list, Bold
from database_requests import get_user, get_user_name, get_leaders
from states import StatisticsState
from keyboards import statistics_kb, start_kb
from logs import log, get_current_time, get_stats_key
from utils import safe_request

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


@router.message(StatisticsState.statistics_type, F.text.in_(states.available_statistics_types + ["На главную"]))
async def select_statistics_type(msg: Message, state: FSMContext):
    if msg.text.lower() == "на главную":
        await state.clear()
        await msg.answer(text.START_MESSAGE, reply_markup=start_kb)
        return

    log("user_journey", timestamp=get_current_time(), user_id=msg.from_user.id,
        event_group="click2button", event_name="statistics_get_type", event_data=get_stats_key(msg.text))

    if msg.text.lower() == "моя":
        # resp = await get_user(msg.from_user.id)
        resp = await safe_request(get_user, msg.from_user.id, msg.from_user.id)
        if resp.status_code != 200:
            log("errors", timestamp=get_current_time(), user_id=msg.from_user.id,
                meta_info="WhoKnows", reason=resp.status_code, category="database")
            await msg.answer(text.ERROR, reply_markup=start_kb)
            return

        user = json.loads(resp.text)

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
        # users = await get_leaders()
        users = await safe_request(get_leaders, msg.from_user.id)

        while len(users["endless"]) != 3:
            users["endless"].append(None)

        while len(users["tasks"]) != 3:
            users["tasks"].append(None)

        content = as_list(Bold(text.LB_HEADER_TASKS), *[
            text.LEADERBOARDS.format(place=i + 1,
                                     leader=users["tasks"][i].username,
                                     score=users["tasks"][i].tasks_answered) if users["tasks"][
                                                                                    i] is not None else "Пусто" for i in
            range(len(users["tasks"]))
        ], sep="\n")

        await msg.answer(**content.as_kwargs(), reply_markup=ReplyKeyboardRemove())

        content = as_list(Bold(text.LB_HEADER_ENDLESS), *[
            text.LEADERBOARDS.format(place=i + 1,
                                     leader=users["endless"][i].username,
                                     score=users["endless"][i].max_unlimited_score) if users["endless"][
                                                                                           i] is not None else "Пусто"
            for i in
            range(len(users["endless"]))
        ], sep="\n")

        await msg.answer(**content.as_kwargs(), reply_markup=start_kb)

    await state.clear()


@router.message(StatisticsState.seek_by_username)
async def find_by_username(msg: Message, state: FSMContext):
    log("user_journey", timestamp=get_current_time(), user_id=msg.from_user.id,
        event_group="kb_enter", event_name="statistics_get_by_name", event_data=msg.text)

    # resp = await get_user_name(msg.text)
    resp = await safe_request(get_user_name, msg.from_user.id, msg.text)

    if resp.status_code != 200:
        log("errors", timestamp=get_current_time(), user_id=msg.from_user.id,
            meta_info="WhoKnows", reason=resp.status_code, category="database")
        await msg.answer(text.ERROR, reply_markup=start_kb)
        return

    user = json.loads(resp.text)

    await msg.answer(text.RESULTS_ELSE.format(user['username'],
                                              user['correct_answers'],
                                              user['correct_answers'] / user['tasks_answered'],
                                              user['max_unlimited_score']),
                     reply_markup=start_kb)
    await state.clear()
