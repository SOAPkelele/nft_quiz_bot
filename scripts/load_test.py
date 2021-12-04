from dataclasses import dataclass, field
from typing import List
import asyncio

import pandas as pd
from asyncpg import Pool, create_pool

from app.utils.config_reader import DB, load_config
from app.utils.db.base import DatabaseBase


@dataclass
class QuestionText:
    question: str
    lang: str


@dataclass
class Question:
    id: int
    test_id: int
    question_texts: List[QuestionText] = field(init=False, default=None)


@dataclass
class AnswerText:
    answer: str
    lang: str


@dataclass
class Answer:
    id: int
    question_id: int
    is_true: bool
    answer_texts: List[AnswerText] = field(init=False, default=None)


class Database(DatabaseBase):
    def __init__(self, pool: Pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls, db_config: DB):
        pool = await create_pool(**db_config.__dict__)
        return cls(pool)

    async def add_test(self):
        sql = """INSERT INTO tests (id, status)
                    VALUES (default, default)
                    RETURNING id"""
        res = await self.pool.fetchval(sql)
        print(f"ID OF CREATED TEST: {res}")
        return res

    async def add_test_text(self, name, description, lang, test_id):
        sql = """INSERT INTO test_texts (name, description, lang, test_id)
                            VALUES ($1, $2, $3, $4)
                            RETURNING id"""
        res = await self.pool.fetchval(sql, *(name, description, lang, test_id))
        print(f"ID OF CREATED TEST_TEXT: {res}")
        return res

    async def add_question(self, test_id):
        sql = """INSERT INTO questions (test_id)
                                    VALUES ($1)
                                    RETURNING id"""
        res = await self.pool.fetchval(sql, *(test_id,))
        print(f"ID OF CREATED QUESTION: {res}")
        return res

    async def add_question_text(self, question, lang, question_id):
        sql = """INSERT INTO question_texts (question, lang, question_id)
                                    VALUES ($1, $2, $3)
                                    RETURNING id"""
        res = await self.pool.fetchval(sql, *(question, lang, question_id))
        print(f"ID OF CREATED QUESTION_TEXT: {res}")
        return res

    async def add_answer(self, question_id, is_true):
        sql = """INSERT INTO answers (question_id, is_true)
                                    VALUES ($1, $2)
                                    RETURNING id"""
        res = await self.pool.fetchval(sql, *(question_id, is_true))
        print(f"ID OF CREATED ANSWER: {res}")
        return res

    async def add_answer_text(self, answer_id, answer, lang):
        sql = """INSERT INTO answer_texts (answer_id, answer, lang)
                                    VALUES ($1, $2, $3)
                                    RETURNING id"""
        res = await self.pool.fetchval(sql, *(answer_id, answer, lang))
        print(f"ID OF CREATED ANSWER TEXT: {res}")
        return res


async def main():
    FILE_NAME = "TEST_1.csv"

    NAME_INDEX = 0
    DESCRIPTION_INDEX = 1

    languages = ["ru", "en", "es", "pt"]

    # ADD TEST, THEN TEST TEXTS

    df = pd.read_csv(FILE_NAME)

    config = load_config()
    db: Database = await Database.create(db_config=config.db)

    test_id = await db.add_test()

    NAMES = df.iloc[NAME_INDEX]
    DESCRIPTIONS = df.iloc[DESCRIPTION_INDEX]

    for language in languages:
        await db.add_test_text(test_id=test_id, lang=language, name=NAMES[language], description=DESCRIPTIONS[language])

    questions = []

    row_count = df.shape[0]

    for i in range(2, row_count):
        # Находим вопрос
        if "вопрос" in str(df.iloc[i]["ru"]).lower():
            question_id = await db.add_question(test_id=test_id)

            # первая строка это сам вопрос
            QUESTIONS = df.iloc[i + 1]
            for language in languages:
                await db.add_question_text(question=QUESTIONS[language], lang=language, question_id=question_id)

            FLAG = True
            # дальше идут варианты ответов
            for answers in range(i + 2, row_count):
                # условие выхода это или конец таблицы или начало след вопроса
                if "вопрос" in str(df.iloc[answers]["ru"]).lower():
                    break

                answer_id = await db.add_answer(question_id=question_id, is_true=FLAG)
                FLAG = False
                ANSWERS = df.iloc[answers]

                for language in languages:
                    await db.add_answer_text(answer_id=answer_id, lang=language, answer=ANSWERS[language])

                # TODO write answers to db


if __name__ == "__main__":
    (asyncio.get_event_loop()).run_until_complete(main())
