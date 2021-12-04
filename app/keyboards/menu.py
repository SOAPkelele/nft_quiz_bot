from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from app.settings import i18n

_ = i18n.gettext

menu_callback = CallbackData("MENU", "action")
back_to_menu_button = InlineKeyboardButton(_("Вернуться назад"), callback_data="BACK_TO_MENU")

menu_keyboard = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(_("Узнать больше о LocalTrade"),
                                 callback_data=menu_callback.new(action="LOCALTRADE_INFO"))
        ],
        [
            InlineKeyboardButton(_("Доступные тесты"),
                                 callback_data=menu_callback.new(action="AVAILABLE_TESTS"))
        ],
        [
            InlineKeyboardButton(_("Пройденные тесты"),
                                 callback_data=menu_callback.new(action="FINISHED_TESTS"))
        ],
        [
            InlineKeyboardButton(_("Сменить язык"),
                                 callback_data=menu_callback.new(action="CHANGE_LANGUAGE"))
        ]

    ]
)

back_to_menu_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            back_to_menu_button
        ]
    ]
)
