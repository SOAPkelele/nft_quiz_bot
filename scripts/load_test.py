from dataclasses import dataclass, field
from typing import List

import pandas as pd
from asyncpg import Pool, create_pool

from app.utils.config_reader import DB
from app.utils.db.base import DatabaseBase

NAME_INDEX = 0
DESCRIPTION_INDEX = 1


class Database(DatabaseBase):
    def __init__(self, pool: Pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls, db_config: DB):
        pool = await create_pool(**db_config.__dict__)
        return cls(pool)

    def add_test(self):
        pass

    def add_test_text(self):
        pass

    def add_question(self):
        pass

    def add_question_text(self):
        pass

    def add_answer(self):
        pass

    def add_answer_text(self):
        pass


def add_test():
    print("Created test")
    return 1


def add_test_text(test_id, name, description, lang):
    pass


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


if __name__ == "__main__":
    FILE_NAME = "TEST_1.csv"

    languages = ["ru", "en", "es", "pt"]

    # ADD TEST, THEN TEST TEXTS

    df = pd.read_csv(FILE_NAME)
    print(df.shape)

    # TODO write test to db
    test = add_test()

    NAMES = df.iloc[NAME_INDEX]
    DESCRIPTIONS = df.iloc[DESCRIPTION_INDEX]

    for language in languages:
        add_test_text(test_id=test, lang=language, name=NAMES[language], description=DESCRIPTIONS[language])

    questions = []

    row_count = df.shape[0]

    for i in range(2, row_count):
        # Находим вопрос
        if "вопрос" in str(df.iloc[i]["ru"]).lower():
            question = Question(test_id=test, id=1)
            question_texts = []

            # первая строка это сам вопрос
            QUESTIONS = df.iloc[i + 1]
            for language in languages:
                question_texts.append(QuestionText(question=QUESTIONS[language], lang=language))
            question.question_texts = question_texts

            print(question)

            # TODO write question to db

            FLAG = True
            # дальше идут варианты ответов
            for answers in range(i + 2, row_count):
                # условие выхода это или конец таблицы или начало след вопроса
                if "вопрос" in str(df.iloc[answers]["ru"]).lower():
                    break

                answer = Answer(id=1,
                                question_id=question.id,
                                is_true=FLAG)
                FLAG = False
                ANSWERS = df.iloc[answers]
                answer_texts = []
                for language in languages:
                    answer_texts.append(AnswerText(answer=ANSWERS[language], lang=language))
                answer.answer_texts = answer_texts
                print(answer)

                # TODO write answers to db
