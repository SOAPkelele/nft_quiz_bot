from app.middlewares.i18n import I18nMiddleware
from app.settings import BASE_DIR

I18N_DOMAIN = "quiz_bot"
LOCALES_DIR = BASE_DIR / "locales"

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR, default="ru")
