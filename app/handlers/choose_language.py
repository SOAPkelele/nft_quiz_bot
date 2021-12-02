from typing import Dict

from aiogram import types
from loguru import logger

from app.handlers.menu.main_menu import send_menu
from app.settings import DB_KEY, i18n
from app.utils import delete_message
from app.utils.db import Database

_ = i18n.gettext


async def choose_language_handler(call: types.CallbackQuery, callback_data: Dict):
    lang = callback_data.get("lang")

    logger.info(f"User [{call.from_user.id}] chose lang: {lang}")

    await call.answer(cache_time=60)
    await delete_message(call.message)
    await set_language(call, lang=lang)
    await send_menu(call.message)


async def set_language(call: types.CallbackQuery, lang: str):
    db: Database = call.bot[DB_KEY]
    await db.set_user_lang(user_id=call.from_user.id, lang=lang)
