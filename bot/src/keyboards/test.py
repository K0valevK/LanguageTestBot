from aiogram import types
from states import available_test_diff, available_test_types

start_kb = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="/test"),
        types.KeyboardButton(text="/statistics"),
        types.KeyboardButton(text="/help")
    ],
], resize_keyboard=True, input_field_placeholder="Выберите команду")

test_kb = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text=i) for i in available_test_types
    ],
], resize_keyboard=True, input_field_placeholder="Выберите режим")

difficulty_kb = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text=i) for i in available_test_diff
    ],
], resize_keyboard=True, input_field_placeholder="Выберите сложность")
