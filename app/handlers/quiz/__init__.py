from aiogram import Dispatcher

from .quiz import begin_quiz_handler, poll_answer_handler
from ...keyboards.inline import start_test_callback
from ...states import TestProgress


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(begin_quiz_handler, start_test_callback.filter())

    dp.register_poll_answer_handler(poll_answer_handler)  # , state=TestProgress.IN_PROGRESS)
