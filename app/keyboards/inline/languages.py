from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

lang_callback = CallbackData("LANG", "lang")

language_keyboard = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton("Русский 🇷🇺", callback_data=lang_callback.new(lang="ru"))],
        [
            InlineKeyboardButton("English 🇬🇧", callback_data=lang_callback.new(lang="en"))
        ],
        [
            InlineKeyboardButton("Español 🇪🇸", callback_data=lang_callback.new(lang="es"))
        ],
        [
            InlineKeyboardButton("Portugués 🇵🇹", callback_data=lang_callback.new(lang="pt"))
        ]

    ]
)
