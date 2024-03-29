from aiogram.filters.state import StatesGroup, State


available_statistics_types = ["Моя", "Лидеры"]


class Statistics(StatesGroup):
    statistics_type = State()
