from typing import Dict

from aiogram import types
from aiogram.utils.callback_data import CallbackData
from loguru import logger

from app.keyboards import MenuKb
from app.misc import i18n
from app.settings import DB_KEY
from app.utils.db import Database

gettext = i18n.gettext


async def finished_tests_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to check finished tests")
    await call.answer()

    finished_tests = await get_finished_tests(call.bot[DB_KEY], user_id=call.from_user.id)

    await call.message.edit_text(finished_tests, reply_markup=MenuKb().back_to_menu(gettext))


async def available_tests_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to check available tests")
    await call.answer()

    text, keyboard = await get_available_tests(db=call.bot[DB_KEY], user_id=call.from_user.id)

    await call.message.edit_text(text, reply_markup=keyboard)


async def show_test_handler(call: types.CallbackQuery, callback_data: Dict):
    test_id = int(callback_data.get("test_id"))
    logger.info(f"User [{call.from_user.id}] wants to check test [ID:{test_id}]")
    await call.answer()

    test = await call.bot[DB_KEY].get_test(test_id=test_id, user_id=call.from_user.id)

    await call.message.edit_text(test.preview, reply_markup=MenuKb().start_test(test_id, gettext))


choose_test_callback = CallbackData("CHOOSE_TEST", "test_id")


async def get_available_tests(db: Database, user_id: int):
    tests = await db.get_available_tests(user_id)

    message = [gettext("Доступные тесты:")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    if tests:
        test_names = []
        for i, test in enumerate(tests):
            test_names.append("#{number}. {test_name}".format(number=i + 1, test_name=test.name))
            keyboard.row(types.InlineKeyboardButton(gettext("#{test_num}. {title}").format(test_num=i + 1,
                                                                                           title=test.title),
                                                    callback_data=choose_test_callback.new(test_id=test.id)))
        message.append("\n".join(test_names))
    else:
        message.append(gettext("Вы прошли все тесты!"))
    keyboard.row(types.InlineKeyboardButton(gettext("Вернуться назад"),
                                            callback_data=MenuKb.callback_data.new("BACK_TO_MENU")))

    return "\n\n".join(message), keyboard


async def get_finished_tests(db: Database, user_id: int):
    scores = await db.get_user_scores(user_id=user_id)

    if not scores:
        return gettext("Вы не прошли ни одного теста!")

    msg = []
    for test_num, score in enumerate(scores):
        sub_msg = [gettext("<b>Тест #{test_num}</b>").format(test_num=test_num + 1),
                   gettext("Поздравляем! "
                           "Вы ответили правильно на <b>{correct_answers}</b> "
                           "вопросов из <b>{total_questions}</b>. "
                           "Вы заработали <b>{earned_points}</b> баллов. "
                           "Вы круче <b>{percent_better}%</b> юзеров.").format(correct_answers=score.correct_answers,
                                                                               total_questions=score.total_questions,
                                                                               earned_points=score.earned_points,
                                                                               percent_better=int(
                                                                                   score.percent_better))]
        msg.append("\n".join(sub_msg))
    return "\n\n".join(msg)
