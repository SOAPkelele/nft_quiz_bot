from typing import Dict

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loguru import logger

from app.keyboards import back_to_menu_button, start_test_keyboard, back_to_menu_keyboard
from app.settings import i18n, DB_KEY
from app.utils.db import Database

_ = i18n.gettext


async def finished_tests_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to check finished tests")
    await call.answer()

    finished_tests = await get_finished_tests(call.bot[DB_KEY], user_id=call.from_user.id)

    await call.message.edit_text(finished_tests, reply_markup=back_to_menu_keyboard)


async def available_tests_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to check available tests")
    await call.answer()

    text, keyboard = await get_available_tests(db=call.bot[DB_KEY], user_id=call.from_user.id)

    await call.message.edit_text(text, reply_markup=keyboard)


async def show_test_handler(call: types.CallbackQuery, callback_data: Dict):
    test_id = int(callback_data.get("test_id"))
    logger.info(f"User [{call.from_user.id}] wants to check test [ID:{test_id}]")
    await call.answer()

    text, keyboard = await get_test(db=call.bot[DB_KEY], user_id=call.from_user.id, test_id=test_id)

    await call.message.edit_text(text, reply_markup=keyboard)


choose_test_callback = CallbackData("CHOOSE_TEST", "test_id")


async def get_available_tests(db: Database, user_id: int):
    tests = await db.get_available_tests(user_id)

    message = [_("Доступные тесты:")]
    keyboard = InlineKeyboardMarkup(row_width=1)

    if tests:
        test_names = []
        for i, test in enumerate(tests):
            test_names.append("#{number}. {test_name}".format(number=i + 1, test_name=test.name))
            keyboard.row(InlineKeyboardButton(_("Тест #{test_num}").format(test_num=i + 1),
                                              callback_data=choose_test_callback.new(test_id=test.id)))
        message.append("\n".join(test_names))
    else:
        message.append(_("Вы прошли все тесты!"))
    keyboard.row(back_to_menu_button)

    return "\n\n".join(message), keyboard


async def get_test(db: Database, test_id: int, user_id: int):
    test = await db.get_test(test_id=test_id, user_id=user_id)

    return test.preview, start_test_keyboard(test_id)


async def get_finished_tests(db: Database, user_id: int):
    scores = await db.get_user_scores(user_id=user_id)

    if not scores:
        return "Вы не прошли ни одного теста!"

    msg = []
    for test_num, score in enumerate(scores):
        sub_msg = [_("<b>Тест #{test_num}</b>").format(test_num=test_num + 1),
                   _("Поздравляем! "
                     "Вы ответили правильно на <b>{correct_answers}</b> "
                     "вопросов из <b>{total_questions}</b>. "
                     "Вы заработали <b>{earned_points}</b> баллов. "
                     "Вы круче <b>{percent_better}%</b> юзеров.").
                       format(correct_answers=score.correct_answers,
                              total_questions=score.total_questions,
                              earned_points=score.earned_points,
                              percent_better=int(score.percent_better))]
        msg.append("\n".join(sub_msg))
    return "\n\n".join(msg)
