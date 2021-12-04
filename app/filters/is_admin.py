from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.settings import APP_CONFIG_KEY


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        return str(message.from_user.id) in message.bot[APP_CONFIG_KEY].admins
