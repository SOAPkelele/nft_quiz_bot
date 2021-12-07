from aiogram import Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from loguru import logger

from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    logger.info("Configuring middlewares...")
    from app.misc import i18n

    dp.middleware.setup(EnvironmentMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(i18n)
