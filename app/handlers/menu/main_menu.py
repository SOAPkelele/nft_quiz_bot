from aiogram import types
from loguru import logger

from app.handlers.start import send_language_keyboard
from app.keyboards.inline import menu_keyboard, back_to_menu_keyboard
from app.settings import i18n
from app.utils import delete_message

_ = i18n.gettext


async def menu_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] requested menu")
    await call.answer(cache_time=60)
    await delete_message(call.message)
    await send_menu(call.message)


# helper
async def send_menu(message: types.Message):
    await message.answer("***bot name***", reply_markup=menu_keyboard)


async def learn_more_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to learn more about LocalTrade")
    await call.message.edit_text(_("Информация о LocalTrade"), reply_markup=back_to_menu_keyboard)


async def set_language_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to change lang")
    await delete_message(call.message)
    await send_language_keyboard(call.message)
