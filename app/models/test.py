from dataclasses import dataclass

from aiogram.utils.markdown import hbold


@dataclass
class Test:
    id: int
    name: str
    description: str

    @property
    def preview(self):
        return "\n\n".join([hbold(self.name), self.description])


@dataclass
class TestScore:
    correct_answers: int
    total_questions: int
    earned_points: int
    percent_better: int
