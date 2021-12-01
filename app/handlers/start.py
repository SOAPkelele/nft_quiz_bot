from aiogram import types
from asyncpg.exceptions import UniqueViolationError
from loguru import logger

from app.keyboards.inline import language_keyboard
from app.settings import DB_KEY, i18n
from app.utils.db import Database

_ = i18n.gettext


async def start_handler(message: types.Message):
    logger.info(f"User [{message.from_user.id}] started bot")
    await message.answer(_("Выберите ваш язык"), reply_markup=language_keyboard)
    await register_user(message=message)


async def register_user(message: types.Message):
    try:
        db: Database = message.bot[DB_KEY]
        await db.add_user(telegram_id=message.from_user.id,
                          username=message.from_user.username,
                          full_name=message.from_user.full_name,
                          lang=message.from_user.language_code)
    except UniqueViolationError:
        logger.info(f"User [{message.from_user.id}] already registered")

    # user_profile_msg = profile_msg(message=message)
    # await message.bot.send_message(chat_id=message.bot[APP_CONFIG_KEY].notification_chat_id, text=user_profile_msg)

# def profile_msg(message: types.Message):
#     return "\n".join([
#         "#new_user",
#         f"<b>id</b>: {hcode(message.from_user.id)}",
#         f"<b>User</b>: {(message.from_user.get_mention(as_html=True))}",
#         f"<b>Name</b>: {hcode(message.from_user.full_name)}",
#         f"<b>Username</b>: {hcode(message.from_user.username)}",
#         f"<b>Locale</b>: {hcode(message.from_user.language_code)}"
#     ])
