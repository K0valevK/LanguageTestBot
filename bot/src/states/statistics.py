from aiogram.filters.state import StatesGroup, State


available_statistics_types = ["Моя", "Найти по username", "Лидеры"]


class Statistics(StatesGroup):
    statistics_type = State()
    seek_by_username = State()
