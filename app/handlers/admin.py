import asyncio
import concurrent.futures
import functools
import os
from typing import Dict

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils.callback_data import CallbackData
from loguru import logger

from app.settings import DB_KEY, FILES_DIR
from app.utils import delete_message
from app.utils.db import Database

test_stat_callback = CallbackData("STAT", "test_id")


async def stats_handler(message: types.Message):
    logger.info(f"User [{message.from_user.id}] requested stats")
    tests = await message.bot[DB_KEY].get_all_tests()

    if not tests:
        return await message.answer(f"В базе нет тестов")

    msg = ["Выбери статистику по нужному тесту.", ""]
    keyboard = InlineKeyboardMarkup(row_width=1)

    for test in tests:
        msg.append(test.info)
        keyboard.row(InlineKeyboardButton(f"Статистика по тесту [ID:{test.id}]",
                                          callback_data=test_stat_callback.new(test_id=test.id)))
    await message.answer("\n".join(msg), reply_markup=keyboard)


async def send_test_stats_handler(call: types.CallbackQuery, callback_data: Dict):
    await call.answer()
    await call.message.answer("Готовлю таблицу...")
    await delete_message(call.message)

    db: Database = call.bot[DB_KEY]

    test_id = int(callback_data.get("test_id"))
    stats = await db.get_test_stats(test_id=test_id)

    if not stats:
        return "Этот тест еще никто не прошел!"

    data = [{"user_id": record.user_id,
             "username": record.username,
             "full_name": record.full_name,
             "points": record.points}
            for record in stats]

    df = pd.DataFrame.from_records(data)
    filename = FILES_DIR / f"test_{test_id}.xlsx"

    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, functools.partial(df.to_excel,
                                                           filename,
                                                           index=False,
                                                           sheet_name=f"test_{test_id}",
                                                           encoding="utf-8"))
    del df

    await call.message.answer_document(caption=f"#Test_ID_{test_id}", document=InputFile(filename))
    os.remove(filename)


async def cancel_state_handler(message: types.Message, state: FSMContext):
    logger.info(f"User [{message.from_user.id}] canceled state bot")

    await message.answer("Стейт сброшен!")
    await state.finish()
