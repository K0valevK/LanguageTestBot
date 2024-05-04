from aiogram import types
from states import available_statistics_types


statistics_kb = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text=i) for i in available_statistics_types
    ],
    [types.KeyboardButton(text="На главную")],
], resize_keyboard=True, input_field_placeholder="Отображённая статистика")
