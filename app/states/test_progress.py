from aiogram.dispatcher.filters.state import StatesGroup, State

TEST_IN_PROGRESS = "TEST_IN_PROGRESS"


class TestProgress(StatesGroup):
    IN_PROGRESS = State()
