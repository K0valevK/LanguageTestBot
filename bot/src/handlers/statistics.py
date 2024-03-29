from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from database_requests import get_user, create_user, update_user

from states import StatisticsState
from keyboards import statistics_kb

import json
import text
import states

router = Router()


@router.message(Command("statistics"))
async def command_statistics(msg: Message, state: FSMContext):
    await state.set_state(StatisticsState.statistics_type)
    await msg.answer(text.START_STATS_MESSAGE, reply_markup=statistics_kb)


@router.message(StatisticsState.statistics_type, F.text.in_(states.available_statistics_types))
async def select_statistics_type(msg: Message, state: FSMContext):
    if msg.text.lower() == "моя":
        user = json.loads((await get_user(msg.from_user.id)).text)
        await msg.answer(f"Ваши результаты\nКоличество правильных ответов: {user['correct_answers']}\nДоля правильных ответов: {user['correct_answers'] / user['tasks_answered']}",
            reply_markup=ReplyKeyboardRemove())
