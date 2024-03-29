from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from database_requests import get_user, create_user, update_user

from keyboards import start_kb

import text

router = Router()


@router.message(Command("start"))
async def start(msg: Message):
    await msg.answer(text.START_MESSAGE, reply_markup=start_kb)
    await create_user(msg.from_user.id)


@router.message(Command("help"))
async def command_help(msg: Message, state: FSMContext):
    await msg.answer(text.HELP_MESSAGE)
