from pathlib import Path

from aiogram.contrib.middlewares.i18n import I18nMiddleware

APP_CONFIG_KEY = "APP_CONFIG"
DB_KEY = "DB_KEY"

I18N_DOMAIN = "QUIZ_BOT"
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / "locales"

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR, default="en")