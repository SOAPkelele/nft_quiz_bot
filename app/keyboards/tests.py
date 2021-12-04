from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from app.keyboards import menu_callback
from app.settings import i18n

_ = i18n.gettext

start_test_callback = CallbackData("BEGIN_TEST", "test_id")

quiz_callback = CallbackData("QUIZ", "test_id", "question_id")

finish_quiz_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(_("Завершить тест"), callback_data="FINISH_QUIZ")
    ]
])

confirm_finish_quiz_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(_("Да, завершить тест"), callback_data="CONFIRM_FINISH_QUIZ")
    ],
    [
        InlineKeyboardButton(_("Нет, продолжить тест"), callback_data="CONTINUE_QUIZ")
    ]
])

after_quiz_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(_("Главное меню"),
                                 callback_data=menu_callback.new(action="BACK_TO_MENU"))
        ],
        [
            InlineKeyboardButton(_("Пройти другой тест"),
                                 callback_data=menu_callback.new(action="AVAILABLE_TESTS"))
        ]
    ]
)


def start_test_keyboard(test_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.row(InlineKeyboardButton(_("Начать тест"), callback_data=start_test_callback.new(test_id=test_id)))
    keyboard.row(InlineKeyboardButton(_("Закрыть тест"), callback_data=menu_callback.new(action="AVAILABLE_TESTS")))

    return keyboard
