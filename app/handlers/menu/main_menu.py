from aiogram import types
from loguru import logger

from app.handlers.start import send_language_keyboard
from app.keyboards import MenuKb
from app.misc import i18n
from app.settings import MENU_MESSAGE
from app.utils import delete_message

i18n = i18n.gettext


async def menu_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] requested menu")
    await call.answer(cache_time=60)
    await delete_message(call.message)
    await call.message.answer(MENU_MESSAGE, reply_markup=MenuKb().main(i18n))


async def learn_more_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to learn more about LocalTrade")
    await call.message.edit_text(i18n("Информация о LocalTrade"), reply_markup=MenuKb().back_to_menu(i18n))


async def set_language_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to change lang")
    await delete_message(call.message)
    await send_language_keyboard(call.message)
