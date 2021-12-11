import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling
from loguru import logger

from app import filters, middlewares, handlers
from app.settings import APP_CONFIG_KEY, DB_KEY, BOT_DISPATCHER_KEY
from app.utils.config_reader import load_config
from app.utils.default_commands import setup_default_commands
from app.utils.logger import setup_logger
from app.utils.notify_admins import notify_admins
from app.utils.db.postgresql import Database


async def on_startup(dp):
    filters.setup(dp)
    handlers.setup(dp)
    middlewares.setup(dp)

    await setup_default_commands(dp)
    await notify_admins([dp.bot[APP_CONFIG_KEY].notification_chat_id])


def get_handled_updates_list(dp: Dispatcher) -> list:
    """
    Here we collect only the needed updates for bot based on already registered handlers types.
    This way Telegram doesn't send unwanted updates and bot doesn't have to proceed them.
    :param dp: Dispatcher
    :return: a list of registered handlers types
    """
    available_updates = (
        "callback_query_handlers", "chat_member_handlers", "edited_channel_post_handlers", "edited_message_handlers",
        "message_handlers", "my_chat_member_handlers", "poll_answer_handlers",
    )
    return [item.replace("_handlers", "") for item in available_updates
            if len(dp.__getattribute__(item).handlers) > 0]


async def on_shutdown(dp):
    logger.warning("Shutting down..")
    await dp.bot[DB_KEY].pool.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.warning("Bye!")


if __name__ == "__main__":
    setup_logger("INFO", ["aiogram.bot.api"])

    config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot=bot, storage=config.fsm_storage.storage)

    bot[APP_CONFIG_KEY] = config
    bot[BOT_DISPATCHER_KEY] = dp
    bot[DB_KEY] = asyncio.get_event_loop().run_until_complete(Database.create(db_config=config.db))

    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown,
                  allowed_updates=get_handled_updates_list(dp),
                  skip_updates=config.skip_updates)
