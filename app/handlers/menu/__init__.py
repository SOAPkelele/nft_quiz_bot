from aiogram import Dispatcher
from loguru import logger

from .main_menu import menu_handler, learn_more_handler, set_language_handler
from .tests_menu import finished_tests_handler, available_tests_handler, choose_test_callback
from ...keyboards import MenuKb
from .tests_menu import show_test_handler


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(menu_handler, MenuKb.callback_data.filter(action="BACK_TO_MENU"))

    dp.register_callback_query_handler(learn_more_handler, MenuKb.callback_data.filter(action="LOCALTRADE_INFO"))

    dp.register_callback_query_handler(set_language_handler, MenuKb.callback_data.filter(action="CHANGE_LANGUAGE"))

    dp.register_callback_query_handler(finished_tests_handler, MenuKb.callback_data.filter(action="FINISHED_TESTS"))

    dp.register_callback_query_handler(available_tests_handler, MenuKb.callback_data.filter(action="AVAILABLE_TESTS"))

    dp.register_callback_query_handler(show_test_handler, choose_test_callback.filter())

    logger.info("Menu handlers configured")
