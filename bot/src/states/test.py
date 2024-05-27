from aiogram.filters.state import StatesGroup, State


available_test_types = ["По уровню сложности", "Бесконечный"]
available_test_diff = ["1", "2", "3", "4", "5"]


class Testing(StatesGroup):
    test_type = State()


class LeveledTest(StatesGroup):
    test_difficulty = State()
    in_progress = State()


class EndlessTest(StatesGroup):
    in_progress = State()
