from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from loguru import logger

from .choose_language import choose_language_handler
from .error_handler import errors_handler
from .start import start_handler
from ..keyboards.inline.languages import lang_callback


def setup(dp: Dispatcher):
    # start
    dp.register_message_handler(start_handler, CommandStart(encoded=True))

    # catch language
    dp.register_callback_query_handler(choose_language_handler, lang_callback.filter())

    # catch all errors
    dp.register_errors_handler(errors_handler)

    logger.info("Handlers are successfully configured")
