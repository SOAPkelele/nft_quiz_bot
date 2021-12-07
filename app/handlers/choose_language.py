from typing import Dict

from aiogram import types
from loguru import logger

from app.keyboards import MenuKb
from app.settings import DB_KEY, MENU_MESSAGE
from app.utils import delete_message
from ..misc import i18n


async def choose_language_handler(call: types.CallbackQuery, callback_data: Dict):
    lang = callback_data.get("lang")
    logger.info(f"User [{call.from_user.id}] chose lang: {lang}")
    await call.answer(cache_time=60)
    await delete_message(call.message)
    await call.bot[DB_KEY].set_user_lang(user_id=call.from_user.id, lang=lang)
    await call.message.answer(MENU_MESSAGE, reply_markup=MenuKb().main(i18n.gettext, lang))
