from aiogram import types

from loguru import logger

from app.settings import APP_CONFIG_KEY

from aiogram.types import BotCommandScopeChat


async def setup_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start bot")
        ]
    )

    for admin in dp.bot[APP_CONFIG_KEY].admins:
        logger.info(admin)
        await dp.bot.set_my_commands(
            [
                types.BotCommand("start", "start bot"),
                types.BotCommand("stats", "Результаты тестов (admin)"),
                types.BotCommand("refresh", "Сбросить свою статистику (admin)")
            ],
            scope=BotCommandScopeChat(admin)
        )

    logger.info('Standard commands are successfully configured')
