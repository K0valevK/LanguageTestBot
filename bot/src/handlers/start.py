from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from database_requests import create_user
from keyboards import start_kb
from logs import log, get_current_time

import text

router = Router()


@router.message(Command("start"))
async def start(msg: Message):
    log("user_journey", timestamp=get_current_time(), user_id=msg.from_user.id,
        event_group="click2button", event_name="start", event_data="None")

    await msg.answer(text.START_MESSAGE, reply_markup=start_kb)
    await create_user(msg.from_user.id, msg.from_user.username)


@router.message(Command("help"))
async def command_help(msg: Message, state: FSMContext):
    log("user_journey", timestamp=get_current_time(), user_id=msg.from_user.id,
        event_group="click2button", event_name="help", event_data="None")

    await msg.answer(text.HELP_MESSAGE)
