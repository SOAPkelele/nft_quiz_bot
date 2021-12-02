from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from app.keyboards.inline.menu import menu_callback
from app.settings import i18n

start_test_callback = CallbackData("BEGIN_TEST", "test_id")

quiz_callback = CallbackData("QUIZ", "test_id", "question_id")

_ = i18n.gettext


def start_test_keyboard(test_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.row(InlineKeyboardButton(_("Начать тест"), callback_data=start_test_callback.new(test_id=test_id)))
    keyboard.row(InlineKeyboardButton(_("Закрыть тест"), callback_data=menu_callback.new(action="AVAILABLE_TESTS")))

    return keyboard


finish_quiz_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(_("Завершить тест"), callback_data="FINISH_QUIZ")
    ]
])
