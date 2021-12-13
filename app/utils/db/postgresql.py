from random import shuffle
from typing import List, Optional

from asyncpg import create_pool
from asyncpg.pool import Pool
from loguru import logger

from app.models import Test, Question, Answer, TestScore, TestStats
from app.utils.config_reader import DB
from app.utils.db.base import DatabaseBase


class Database(DatabaseBase):
    def __init__(self, pool: Pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls, db_config: DB):
        logger.info("Connecting to DB...")
        pool = await create_pool(**db_config.__dict__)
        return cls(pool)

    """USERS"""

    async def add_user(self, **kwargs):
        sql, values = self._insert_args(table="users", column_values=kwargs)
        await self.pool.execute(sql, *values)

    async def get_user_lang(self, user_id: int):
        sql, values = self._select_where_args("users", ["lang"], {"user_id": user_id})
        res = await self.pool.fetchrow(sql, *values)
        return res.get("lang") if res else None

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

    """TESTS"""

    async def get_finished_tests(self, user_id: int):
        sql = """"""
        values = (user_id,)
        await self.pool.fetch(sql, *values)

    async def get_available_tests(self, user_id: int) -> Optional[List[Test]]:
        sql = """SELECT t.id, t.title, tt.name, tt.description
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
        sql = """SELECT t.id, t.title, tt.name, tt.description
                FROM tests t
                         JOIN test_texts tt ON t.id = tt.test_id
                WHERE tt.lang = (SELECT lang FROM users WHERE user_id = $1)
                  AND t.id = $2"""
        values = (user_id, test_id)
        res = await self.pool.fetchrow(sql, *values)

        return Test(**res) if res else None

    """QUESTIONS"""

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

    async def get_user_scores(self, user_id: int) -> Optional[List[TestScore]]:
        sql = """SELECT test_id,
                       correct_answers,
                       earned_points,
                       total_questions,
                       percent_better
                FROM (
                         SELECT ut1.user_id,
                                ut1.test_id,
                                ut1.correct_answers,
                                ut1.points                                      as earned_points,
                                CASE
                                    WHEN ut1.points = max(ut1.points) OVER (PARTITION BY ut1.test_id) THEN 100
                                    ELSE round((count(ut2.user_id) FILTER ( WHERE ut1.points > ut2.points )::NUMERIC /
                                                count(ut1.user_id) OVER (PARTITION BY ut1.test_id)), 2) * 100
                                    END                                         AS percent_better,
                                (SELECT count(q.id)
                                 FROM tests t
                                          JOIN questions q ON t.id = q.test_id) AS total_questions
                         FROM user_tests ut1
                                  JOIN user_tests ut2 ON ut1.test_id = ut2.test_id
                         GROUP BY ut1.test_id, ut1.user_id, ut1.correct_answers, ut1.points) stats
                WHERE stats.user_id = $1
                ORDER BY test_id DESC"""
        values = (user_id,)
        res = await self.pool.fetch(sql, *values)

        return [TestScore(**score) for score in res] if res else None

    async def get_user_score(self, user_id: int, test_id: int) -> TestScore:
        sql = """SELECT test_id,
                       correct_answers,
                       earned_points,
                       total_questions,
                       percent_better
                FROM (
                         SELECT ut1.user_id,
                                ut1.test_id,
                                ut1.correct_answers,
                                ut1.points                                      as earned_points,
                                CASE
                                    WHEN ut1.points = max(ut1.points) OVER (PARTITION BY ut1.test_id) THEN 100
                                    ELSE round((count(ut2.user_id) FILTER ( WHERE ut1.points > ut2.points )::NUMERIC /
                                                count(ut1.user_id) OVER (PARTITION BY ut1.test_id)), 2) * 100
                                    END                                         AS percent_better,
                                (SELECT count(q.id)
                                 FROM tests t
                                          JOIN questions q ON t.id = q.test_id) AS total_questions
                         FROM user_tests ut1
                                  JOIN user_tests ut2 ON ut1.test_id = ut2.test_id
                         GROUP BY ut1.test_id, ut1.user_id, ut1.correct_answers, ut1.points) stats
                WHERE stats.user_id = $1 and stats.test_id = $2"""
        values = (user_id, test_id)
        res = await self.pool.fetchrow(sql, *values)
        return TestScore(**res) if res else None

    """ADMINS"""

    async def get_all_tests(self) -> Optional[List[Test]]:
        sql = """SELECT t.id, t.title, tt.name, tt.description
                    FROM tests t
                             JOIN test_texts tt ON t.id = tt.test_id
                    WHERE lang = 'ru'"""
        res = await self.pool.fetch(sql)
        return [Test(**test) for test in res] if res else None

    async def get_test_stats(self, test_id: int) -> Optional[List[TestStats]]:
        sql = """SELECT u.user_id, u.username, u.full_name, ut.test_id, ut.points
                    FROM user_tests ut
                             join users u on ut.user_id = u.user_id
                    WHERE test_id = $1
                    ORDER BY points DESC"""
        values = (test_id,)
        res = await self.pool.fetch(sql, *values)
        return [TestStats(**stat) for stat in res] if res else None

    async def remove_stats(self, user_id: int):
        sql = """DELETE FROM user_tests
                 WHERE user_id = $1"""
        values = (user_id,)
        await self.pool.execute(sql, *values)
