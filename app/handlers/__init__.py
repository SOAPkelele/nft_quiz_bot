from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, Command
from loguru import logger

from . import menu
from . import quiz
from .admin import cancel_state_handler, stats_handler, send_test_stats_handler, test_stat_callback
from .choose_language import choose_language_handler
from .error_handler import errors_handler
from .start import start_handler
from ..keyboards.languages import lang_callback


def setup(dp: Dispatcher):
    # start
    dp.register_message_handler(start_handler, CommandStart(encoded=True))

    # catch language
    dp.register_callback_query_handler(choose_language_handler, lang_callback.filter())

    menu.setup(dp)
    quiz.setup(dp)

    # admin handlers
    dp.register_message_handler(stats_handler, Command("stats"), is_admin=True)  # TODO add admin filter
    dp.register_callback_query_handler(send_test_stats_handler, test_stat_callback.filter(), is_admin=True)

    # catch all errors
    dp.register_errors_handler(errors_handler)

    # finish state for admins
    dp.register_message_handler(cancel_state_handler, Command("cancel"), state="*", is_admin=True)

    logger.info("Handlers are successfully configured")
