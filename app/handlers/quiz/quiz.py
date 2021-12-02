from typing import Dict

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from loguru import logger

from app.keyboards.inline import finish_quiz_keyboard
from app.models import Question
from app.settings import DB_KEY, BOT_DISPATCHER_KEY
from app.states import TestProgress
from app.utils import remove_kb
from app.utils.db import Database


async def begin_quiz_handler(call: types.CallbackQuery, callback_data: Dict, state: FSMContext):
    await call.answer(cache_time=5)
    test_id = int(callback_data.get("test_id"))
    logger.info(f"User [{call.from_user.id}] started test [ID:{test_id}]")
    await remove_kb(call.message)

    await TestProgress.IN_PROGRESS.set()

    question = await get_poll(db=call.bot[DB_KEY], user_id=call.from_user.id, test_id=test_id, question_number=0)

    msg = await call.message.answer_poll(**question.poll_info, reply_markup=finish_quiz_keyboard)

    await state.update_data(test_id=test_id, question_number=0, question=question, msg_id=msg.message_id)


async def get_poll(db: Database, user_id: int, test_id: int, question_number: int):
    return await db.get_question(user_id=user_id, test_id=test_id, question_number=question_number)


async def poll_answer_handler(poll: types.PollAnswer):
    logger.info(poll)

    # get user data via dispatcher and fsm context
    bot: Bot = poll.bot
    state = bot[BOT_DISPATCHER_KEY].current_state(chat=poll.user.id, user=poll.user.id)
    data = await state.get_data()

    logger.info(data)
    previous_question: Question = data.get("question")
    test_id = int(data.get("test_id"))
    question_number = int(data.get("question_number")) + 1

    # delete reply keyboard for message with previous poll
    await bot.edit_message_reply_markup(chat_id=poll.user.id, message_id=data.get("msg_id"), reply_markup=None)

    new_poll = await get_poll(db=bot[DB_KEY],
                              user_id=poll.user.id,
                              test_id=test_id,
                              question_number=question_number)
    if not new_poll:
        await state.finish()
        return await bot.send_message(text="Вы завершили тест!", chat_id=poll.user.id)
    # dp = Dispatcher.get_current()

    msg = await bot.send_poll(chat_id=poll.user.id, **new_poll.poll_info, reply_markup=finish_quiz_keyboard)

    await state.update_data(test_id=test_id,
                            question_number=question_number + 1,
                            poll=new_poll,
                            msg_id=msg.message_id)
