from aiogram.utils.callback_data import CallbackData

from app.utils.markup_constructor import InlineMarkupConstructor


class LanguageKb(InlineMarkupConstructor):
    callback_data = CallbackData("LANG", "lang")

    def get(self):
        schema = [2, 2]
        actions = [
            {"text": "Русский 🇷🇺", "cb": self.callback_data.new("ru")},
            {"text": "English 🇬🇧", "cb": self.callback_data.new("en")},
            {"text": "Español 🇪🇸", "cb": self.callback_data.new("es")},
            {"text": "Portugués 🇵🇹", "cb": self.callback_data.new("pt")}
        ]
        return self.markup(actions, schema)
