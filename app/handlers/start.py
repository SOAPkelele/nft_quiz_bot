from aiogram import types
from asyncpg.exceptions import UniqueViolationError
from loguru import logger

from app.keyboards import language_keyboard
from app.settings import DB_KEY, i18n
from app.utils.db import Database

_ = i18n.gettext


async def start_handler(message: types.Message):
    logger.info(f"User [{message.from_user.id}] started bot")
    await send_language_keyboard(message)
    await register_user(message=message)


async def send_language_keyboard(message: types.Message):
    await message.answer(_("Выберите ваш язык"), reply_markup=language_keyboard)


async def register_user(message: types.Message):
    try:
        db: Database = message.bot[DB_KEY]
        await db.add_user(user_id=message.from_user.id,
                          username=message.from_user.username,
                          full_name=message.from_user.full_name,
                          lang=message.from_user.language_code)
    except UniqueViolationError:
        logger.info(f"User [{message.from_user.id}] already registered")
