import asyncio
import concurrent.futures
import os
from random import randint
from typing import Dict

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from loguru import logger

from app.keyboards import MenuKb
from app.misc import i18n
from app.settings import DB_KEY, BOT_DISPATCHER_KEY, MENU_MESSAGE
from app.states import TEST_IN_PROGRESS
from app.utils import remove_kb, delete_message, score_photo
from app.utils.db import Database

gettext = i18n.gettext

stickers = [
    "CAACAgIAAxkBAAEM_vths7lWZE7FtA8om64ecMQu5QrSbAACQxIAAhgTeEnLSBhi2slRjSME",
    "CAACAgIAAxkBAAEM_v1hs7sCyOG_e_02fc18L8L7GG5HYQACOhUAAlVDcEk9puNuQcfU1iME",
    "CAACAgIAAxkBAAEM_v9hs7tPvGfu3DupytTtw-h7pOGm2wACBhcAAq7qcUn4rmGC15UJCCME",
    "CAACAgIAAxkBAAEM_wFhs7tn9zGXWE77BVgAAfUNkGrv7xMAAnMVAAITIXlJpldL1tV1M5ojBA",
    "CAACAgIAAxkBAAEM_wNhs7tzrJ0pxXwupwLldvk1NIamfQACVw8AAjGweEm19IdN-slZeiME",
    "CAACAgIAAxkBAAEM_wVhs7t9WvGsIXU3ufX9t0XQw8q1IQAC_hAAAoNReEmAcDje4kiutSME",
    "CAACAgIAAxkBAAEM_wdhs7uHS6VfYMWZ_fjfXtkFVNtoDwACOBMAAvDkeEk9rZwoZbF_FiME",
    "CAACAgIAAxkBAAEM_wlhs7uVCxj8uidqwPUUP5Aokf57kgACkRQAAhmheUm2Hh93Y6juZSME",
    "CAACAgIAAxkBAAEM_wths7uj_9AcS2xXmAZAl8Cl-ChsKgACURUAApc6cUnrvhKxLF--SiME",
    "CAACAgIAAxkBAAEM_w1hs7uukstMP5Ba_kPiWoDYpYWFqgAChw4AAmVseUkhqdUUST25LyME"
]


async def begin_quiz_handler(call: types.CallbackQuery, callback_data: Dict, state: FSMContext):
    test_id = int(callback_data.get("test_id"))
    logger.info(f"User [{call.from_user.id}] started test [ID:{test_id}]")
    await call.answer(cache_time=5)
    await remove_kb(call.message)

    question = await get_poll(db=call.bot[DB_KEY], user_id=call.from_user.id, test_id=test_id, question_number=0)

    await state.set_state(TEST_IN_PROGRESS)

    await send_sticker(chat_id=call.from_user.id, bot=call.bot)
    msg = await call.message.answer_poll(**question.poll_info, reply_markup=MenuKb().finish_quiz(gettext))

    await state.update_data(test_id=test_id,
                            question_number=0,
                            answer_id=question.correct_answer_id,
                            msg_id=msg.message_id)


async def poll_answer_handler(poll: types.PollAnswer):
    # get user data via dispatcher and fsm context
    bot: Bot = poll.bot
    state = bot[BOT_DISPATCHER_KEY].current_state(chat=poll.user.id, user=poll.user.id)
    data = await state.get_data()

    db: Database = bot[DB_KEY]
    test_id = int(data.get("test_id"))
    question_number = int(data.get("question_number", 0))
    previous_question = await get_poll(db=db,
                                       user_id=poll.user.id,
                                       test_id=test_id,
                                       question_number=question_number)
    question_number += 1
    earned_points = int(data.get("points", 0))
    correct_answers = int(data.get("answers", 0))

    # delete reply keyboard for message with previous poll
    await bot.edit_message_reply_markup(chat_id=poll.user.id, message_id=data.get("msg_id"), reply_markup=None)

    if data.get("answer_id") == poll.option_ids[0]:
        earned_points += previous_question.points
        correct_answers += 1
        await bot.send_message(
            text=gettext("Вы заработали <b>{points}</b> баллов!").format(points=previous_question.points),
            chat_id=poll.user.id)
        await state.update_data(points=earned_points,
                                answers=correct_answers)

    new_question = await get_poll(db=db,
                                  user_id=poll.user.id,
                                  test_id=test_id,
                                  question_number=question_number)

    # if no more questions, save stats and finish
    if not new_question:
        await state.finish()
        await save_stats(db=db, bot=bot,
                         user=poll.user, test_id=test_id,
                         correct_answers=correct_answers,
                         earned_points=earned_points)
        return

    await send_sticker(chat_id=poll.user.id, bot=poll.bot)
    msg = await bot.send_poll(chat_id=poll.user.id, **new_question.poll_info,
                              reply_markup=MenuKb().finish_quiz(gettext))

    await state.update_data(test_id=test_id,
                            answer_id=new_question.correct_answer_id,
                            question_number=question_number,
                            msg_id=msg.message_id)


async def finish_test_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to finish test")

    await delete_message(call.message)
    await call.message.answer(gettext("Вы уверены, что хотите преждевременно завершить тест? "
                                      "У вас больше не будет возможности его пройти."),
                              reply_markup=MenuKb().confirm_finishing_quiz(gettext))


async def continue_test_handler(call: types.CallbackQuery, state: FSMContext):
    logger.info(f"User [{call.from_user.id}] wants to continue test")
    await delete_message(call.message)

    data = await state.get_data()

    new_question = await get_poll(db=call.bot[DB_KEY],
                                  user_id=call.from_user.id,
                                  test_id=int(data.get("test_id")),
                                  question_number=int(data.get("question_number")))

    msg = await call.message.answer_poll(**new_question.poll_info, reply_markup=MenuKb().finish_quiz(gettext))

    await state.update_data(msg_id=msg.message_id,
                            answer_id=new_question.correct_answer_id)


async def confirm_finishing_handler(call: types.CallbackQuery, state: FSMContext):
    logger.info(f"User [{call.from_user.id}] confirms to finish test")
    await delete_message(call.message)

    data = await state.get_data()
    bot: Bot = call.bot

    await state.finish()

    await save_stats(db=bot[DB_KEY], bot=bot,
                     user=call.from_user,
                     test_id=int(data.get("test_id")),
                     correct_answers=int(data.get("answers", 0)),
                     earned_points=int(data.get("points", 0)))


async def save_stats(db: Database, bot: Bot,
                     user: types.User, test_id: int, correct_answers: int, earned_points: int):
    """Save user quiz stats then, send final message, then menu"""
    await db.save_user_stats(user_id=user.id,
                             test_id=test_id,
                             correct_answers=correct_answers,
                             points=earned_points)

    score = await db.get_user_score(user_id=user.id, test_id=test_id)
    msg = gettext("Поздравляем, @{username}!\n"
                  "Вы ответили правильно на {correct_answers} "
                  "вопросов из {total_questions}.\n"
                  "Вы заработали {earned_points} баллов.\n"
                  "Вы круче {percent_better}% юзеров.",
                  locale=await db.get_user_lang(user.id) or "en").format(username=user.username,
                                                                         correct_answers=score.correct_answers,
                                                                         total_questions=score.total_questions,
                                                                         earned_points=score.earned_points,
                                                                         percent_better=int(score.percent_better))

    loop = asyncio.get_event_loop()
    try:
        with concurrent.futures.ProcessPoolExecutor() as pool:
            photo_path = await loop.run_in_executor(pool, score_photo, msg, user.id)
        await bot.send_photo(chat_id=user.id, photo=InputFile(photo_path))
        os.remove(photo_path)
    except Exception as exp:
        logger.exception(exp)
        await bot.send_message(chat_id=user.id, text=msg)
    await bot.send_message(chat_id=user.id, text=MENU_MESSAGE, reply_markup=MenuKb().main(gettext))


async def get_poll(db: Database, user_id: int, test_id: int, question_number: int):
    return await db.get_question(user_id=user_id, test_id=test_id, question_number=question_number)


async def send_sticker(chat_id: int, bot: Bot):
    if int(randint(1, 100)) % 2 == 0:
        await bot.send_sticker(chat_id=chat_id, sticker=stickers[randint(0, len(stickers) - 1)])
