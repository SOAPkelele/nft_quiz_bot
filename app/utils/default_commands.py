from aiogram import types
import logging


async def setup_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("menu", "Меню"),
            types.BotCommand("add_workout", "Добавить тренировку"),
            types.BotCommand("add_weight", "Записать вес"),
            types.BotCommand("count_calories", "Рассчитать калории и бжу"),
            types.BotCommand("help", "Справка по командам")
        ]
    )
    logging.info('Standard commands are successfully configured')
