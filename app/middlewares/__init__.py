from aiogram import Dispatcher
from loguru import logger

from .i18n import I18nMiddleware
from .test import MyBase
from .throttling import ThrottlingMiddleware

from aiogram.contrib.middlewares.environment import EnvironmentMiddleware

from ..settings import I18N_DOMAIN, LOCALES_DIR


def setup(dp: Dispatcher):
    logger.info("Configuring middlewares...")
    from app.settings import i18n

    dp.middleware.setup(EnvironmentMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(MyBase())
    dp.middleware.setup(I18nMiddleware(I18N_DOMAIN, LOCALES_DIR, default="en"))
