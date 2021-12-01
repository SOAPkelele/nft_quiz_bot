from aiogram import Dispatcher
from loguru import logger

from .test import MyBase
from .throttling import ThrottlingMiddleware

from aiogram.contrib.middlewares.environment import EnvironmentMiddleware


def setup(dp: Dispatcher):
    logger.info("Configuring middlewares...")
    from app.settings import i18n

    dp.middleware.setup(EnvironmentMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(MyBase())
    dp.middleware.setup(i18n)
