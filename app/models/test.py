from dataclasses import dataclass

from aiogram.utils.markdown import hbold


@dataclass
class Test:
    id: int
    title: str
    name: str
    description: str

    @property
    def preview(self):
        return "\n\n".join([hbold(self.name), self.description])

    @property
    def info(self):
        return f"Тест [ID:{self.id}] \"{self.name}\""


@dataclass
class TestScore:
    test_id: int
    correct_answers: int
    total_questions: int
    earned_points: int
    percent_better: int


@dataclass
class TestStats:
    user_id: int
    username: str
    full_name: str
    test_id: int
    points: int
