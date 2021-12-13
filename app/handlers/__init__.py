from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, Command
from loguru import logger

from app.keyboards import LanguageKb
from . import menu
from . import quiz
from .admin import cancel_state_handler, stats_handler, send_test_stats_handler, test_stat_callback, \
    remove_stats_handler
from .choose_language import choose_language_handler
from .error_handler import errors_handler
from .start import start_handler


def setup(dp: Dispatcher):
    # start
    dp.register_message_handler(start_handler, CommandStart(encoded=True))

    # catch language
    dp.register_callback_query_handler(choose_language_handler, LanguageKb.callback_data.filter())

    menu.setup(dp)
    quiz.setup(dp)

    # admin handlers
    dp.register_message_handler(stats_handler, Command("stats"), is_admin=True)
    dp.register_callback_query_handler(send_test_stats_handler, test_stat_callback.filter(), is_admin=True)
    # finish state for admins
    dp.register_message_handler(cancel_state_handler, Command("cancel"), state="*", is_admin=True)
    # delete admin stats in tests in order to be able to pass them again
    dp.register_message_handler(remove_stats_handler, Command("refresh"), is_admin=True)

    # catch all errors
    dp.register_errors_handler(errors_handler)

    logger.info("Handlers are successfully configured")
