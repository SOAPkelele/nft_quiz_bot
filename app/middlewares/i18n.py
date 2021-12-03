from dataclasses import dataclass, field
from typing import Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware

from app.settings import DB_KEY


@dataclass
class LanguageData:
    flag: str
    title: str
    label: str = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


class I18nMiddleware(BaseI18nMiddleware):
    AVAILABLE_LANGUAGES = {
        "en": LanguageData("🇬🇧", "English"),
        "ru": LanguageData("🇷🇺", "Русский"),
        "es": LanguageData("🇪🇸", "Español"),
        "pt": LanguageData("🇵🇹", "Portugués")
    }

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        update = args[0]
        bot: dict = args[-1]["bot"]

        if isinstance(update, (types.Message, types.CallbackQuery)):
            user: types.User = update.from_user
        elif isinstance(update, types.PollAnswer):
            user: types.User = update.user

        lang = await bot.get(DB_KEY).get_user_lang(user.id) or user.language_code or self.default

        return lang
