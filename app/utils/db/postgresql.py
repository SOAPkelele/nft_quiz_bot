import logging
from typing import List, Optional

from asyncpg import create_pool
from asyncpg.pool import Pool

from app.models import Test, Question, Answer
from app.utils.config_reader import DB
from app.utils.db.base import DatabaseBase
from random import shuffle


class Database(DatabaseBase):
    def __init__(self, pool: Pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls, db_config: DB):
        logging.info("Connecting to DB...")
        pool = await create_pool(**db_config.__dict__)
        return cls(pool)

    async def add_user(self, **kwargs):
        sql, values = self._insert_args(table="users", column_values=kwargs)
        await self.pool.execute(sql, *values)

    async def get_user_lang(self, user_id: int):
        sql, values = self._select_where_args("users", ["lang"], {"user_id": user_id})
        res = await self.pool.fetchrow(sql, *values)
        return res.get("lang")

    async def set_user_lang(self, user_id: int, lang: str):
        sql = """UPDATE users SET lang = $1 WHERE user_id = $2"""
        values = (lang, user_id)
        await self.pool.execute(sql, *values)

    async def save_user_stats(self, user_id: int, test_id: int, correct_answers: int, points: int):
        sql, values = self._insert_args(table="user_tests",
                                        column_values={"user_id": user_id,
                                                       "test_id": test_id,
                                                       "correct_answers": correct_answers,
                                                       "points": points})
        await self.pool.execute(sql, *values)

    async def get_finished_tests(self, user_id: int):
        sql = """"""
        values = (user_id,)
        await self.pool.fetch(sql, *values)

    async def get_available_tests(self, user_id: int) -> Optional[List[Test]]:
        sql = """SELECT t.id, tt.name, tt.description
                    FROM tests t
                             JOIN test_texts tt on t.id = tt.test_id
                    WHERE t.status = 1
                      AND t.id not in (SELECT test_id FROM user_tests WHERE user_id = $1)
                      AND tt.lang = (SELECT lang FROM users WHERE user_id = $2)
                    GROUP BY t.id, tt.name, tt.description
                    ORDER BY t.id"""
        values = (user_id, user_id)
        res = await self.pool.fetch(sql, *values)

        return [Test(**record) for record in res] if res else None

    async def get_test(self, test_id: int, user_id: int) -> Optional[Test]:
        sql = """SELECT t.id, tt.name, tt.description
                FROM tests t
                         JOIN test_texts tt ON t.id = tt.test_id
                WHERE tt.lang = (SELECT lang FROM users WHERE user_id = $1)
                  AND t.id = $2"""
        values = (user_id, test_id)
        res = await self.pool.fetchrow(sql, *values)

        return Test(**res) if res else None

    async def get_question(self, test_id: int, user_id: int, question_number: int) -> Optional[Question]:
        sql_question = """SELECT q.id, qt.question, q.points
                FROM tests t
                         JOIN questions q on q.test_id = t.id
                         JOIN question_texts qt ON q.id = qt.question_id
                WHERE t.id = $1
                  AND qt.lang = (SELECT lang FROM users WHERE user_id = $2)
                OFFSET $3 LIMIT 1"""
        values_question = (test_id, user_id, question_number)
        question_raw = await self.pool.fetchrow(sql_question, *values_question)

        if not question_raw:
            return None

        question = Question(**question_raw)

        sql_answers = """SELECT a.id, at.answer, at.description, a.is_true
                FROM tests t
                         JOIN questions q on q.test_id = t.id
                         JOIN answers a on q.id = a.question_id
                         JOIN answer_texts at on a.id = at.answer_id
                WHERE t.id = $1
                  AND q.id = $2
                  AND at.lang = (SELECT lang FROM users WHERE user_id = $3)"""
        values_answers = (test_id, question.id, user_id)
        answers_raw = await self.pool.fetch(sql_answers, *values_answers)

        answer_options = [Answer(**answer) for answer in answers_raw]
        shuffle(answer_options)

        question.answer_options = answer_options

        return question

    async def get_test_score(self, user_id: int, test_id: int):
        sql = """SELECT ut.correct_answers, count(q.id) AS total_questions, ut.points
FROM user_tests ut
         JOIN tests t ON ut.test_id = t.id
         JOIN questions q ON t.id = q.test_id
GROUP BY ut.correct_answers, ut.points;"""
        values = ()
