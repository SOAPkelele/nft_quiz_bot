from aiogram import Dispatcher

from .quiz import begin_quiz_handler, poll_answer_handler, finish_test_handler, continue_test_handler, \
    confirm_finishing_handler
from ...keyboards import start_test_callback
from ...states import TEST_IN_PROGRESS


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(begin_quiz_handler, start_test_callback.filter())

    dp.register_poll_answer_handler(poll_answer_handler)

    dp.register_callback_query_handler(finish_test_handler, text="FINISH_QUIZ", state=TEST_IN_PROGRESS)

    dp.register_callback_query_handler(continue_test_handler, text="CONTINUE_QUIZ", state=TEST_IN_PROGRESS)

    dp.register_callback_query_handler(confirm_finishing_handler, text="CONFIRM_FINISH_QUIZ", state=TEST_IN_PROGRESS)
