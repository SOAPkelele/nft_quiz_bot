from dataclasses import dataclass, field
from typing import Tuple, Any

from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware
from loguru import logger

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
        # logger.info(args[0])
        user: dict = args[0]["from"]
        data: dict = args[-1]
        lang = await data["bot"].get(DB_KEY).get_user_lang(user["id"]) or user["language_code"] or self.default
        # logger.info(lang)
        return lang
