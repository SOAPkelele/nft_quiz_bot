from typing import Dict

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from loguru import logger

from app.handlers.menu.main_menu import send_menu
from app.keyboards.inline import finish_quiz_keyboard, confirm_finish_quiz_keyboard, menu_keyboard
from app.models import Question
from app.settings import DB_KEY, BOT_DISPATCHER_KEY, i18n
from app.states import TEST_IN_PROGRESS
from app.utils import remove_kb, delete_message
from app.utils.db import Database

_ = i18n.gettext


async def begin_quiz_handler(call: types.CallbackQuery, callback_data: Dict, state: FSMContext):
    await call.answer(cache_time=5)
    test_id = int(callback_data.get("test_id"))
    logger.info(f"User [{call.from_user.id}] started test [ID:{test_id}]")
    await remove_kb(call.message)

    await state.set_state(TEST_IN_PROGRESS)

    question = await get_poll(db=call.bot[DB_KEY], user_id=call.from_user.id, test_id=test_id, question_number=0)

    msg = await call.message.answer_poll(**question.poll_info, reply_markup=finish_quiz_keyboard)

    await state.update_data(test_id=test_id, question_number=0, question=question, msg_id=msg.message_id)


async def get_poll(db: Database, user_id: int, test_id: int, question_number: int):
    return await db.get_question(user_id=user_id, test_id=test_id, question_number=question_number)


async def poll_answer_handler(poll: types.PollAnswer):
    # get user data via dispatcher and fsm context
    bot: Bot = poll.bot
    state = bot[BOT_DISPATCHER_KEY].current_state(chat=poll.user.id, user=poll.user.id)
    data = await state.get_data()

    previous_question: Question = data.get("question")
    test_id = int(data.get("test_id"))
    question_number = int(data.get("question_number")) + 1
    earned_points = int(data.get("points", 0))
    correct_answers = int(data.get("answers", 0))
    db: Database = bot[DB_KEY]

    # delete reply keyboard for message with previous poll
    await bot.edit_message_reply_markup(chat_id=poll.user.id, message_id=data.get("msg_id"), reply_markup=None)

    if poll.option_ids[0] == previous_question.correct_answer_id:
        earned_points += previous_question.points
        correct_answers += 1
        await bot.send_message(text=_("Вы заработали <b>{points}</b> баллов!").format(points=previous_question.points),
                               chat_id=poll.user.id)
        await state.update_data(points=earned_points,
                                answers=correct_answers)

    new_question = await get_poll(db=db,
                                  user_id=poll.user.id,
                                  test_id=test_id,
                                  question_number=question_number)
    if not new_question:
        await state.finish()
        await db.save_user_stats(user_id=poll.user.id,
                                 test_id=test_id,
                                 correct_answers=correct_answers,
                                 points=earned_points)
        await bot.send_message(text=_("Поздравляем! "
                                      "Вы ответили правильно на <b>{correct_answers}</b> "
                                      "вопросов из <b>{total_questions}</b>. "
                                      "Вы заработали <b>{earned_points}</b> баллов. "
                                      "Вы круче <b>{percent_better}%</b> юзеров.").
                               format(correct_answers=correct_answers,
                                      total_questions=question_number,
                                      earned_points=earned_points,
                                      percent_better=100),
                               chat_id=poll.user.id)
        return await bot.send_message(chat_id=poll.user.id, text="***bot name***", reply_markup=menu_keyboard)

    msg = await bot.send_poll(chat_id=poll.user.id, **new_question.poll_info, reply_markup=finish_quiz_keyboard)

    await state.update_data(test_id=test_id,
                            question=new_question,
                            question_number=question_number,
                            msg_id=msg.message_id)


async def finish_test_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to finish test")

    await delete_message(call.message)

    await call.message.answer(_("Вы уверены, что хотите преждевременно завершить тест? "
                                "У вас больше не будет возможности его пройти."),
                              reply_markup=confirm_finish_quiz_keyboard)


async def continue_test_handler(call: types.CallbackQuery, state: FSMContext):
    logger.info(f"User [{call.from_user.id}] wants to continue test")
    await delete_message(call.message)

    data = await state.get_data()

    new_question = await get_poll(db=call.bot[DB_KEY],
                                  user_id=call.from_user.id,
                                  test_id=int(data.get("test_id")),
                                  question_number=int(data.get("question_number")))

    msg = await call.message.answer_poll(**new_question.poll_info, reply_markup=finish_quiz_keyboard)

    await state.update_data(msg_id=msg.message_id)


async def confirm_finishing_handler(call: types.CallbackQuery, state: FSMContext):
    logger.info(f"User [{call.from_user.id}] confirms to finish test")
    await delete_message(call.message)

    bot: Bot = call.bot
    data = await state.get_data()

    question_number = int(data.get("question_number")) + 1
    earned_points = int(data.get("points", 0))
    correct_answers = int(data.get("answers", 0))
    db: Database = bot[DB_KEY]

    await state.finish()
    await db.save_user_stats(user_id=call.from_user.id,
                             test_id=int(data.get("test_id")),
                             correct_answers=correct_answers,
                             points=earned_points)
    await call.message.answer(text=_("Поздравляем! "
                                     "Вы ответили правильно на <b>{correct_answers}</b> "
                                     "вопросов из <b>{total_questions}</b>. "
                                     "Вы заработали <b>{earned_points}</b> баллов. "
                                     "Вы круче <b>{percent_better}%</b> юзеров.").
                              format(correct_answers=correct_answers,
                                     total_questions=question_number,
                                     earned_points=earned_points,
                                     percent_better=100))
    await send_menu(call.message)
