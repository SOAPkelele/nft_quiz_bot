from dataclasses import dataclass, field
from typing import List


@dataclass
class Answer:
    id: int
    answer: str
    description: str
    is_true: bool


@dataclass
class Question:
    id: int
    question: str
    points: str

    answer_options: List[Answer] = field(init=False, default=None)

    @property
    def answer_description(self):
        for answer_option in self.answer_options:
            if answer_option.is_true:
                return answer_option.description

    @property
    def correct_answer_num(self):
        for i, answer_option in enumerate(self.answer_options):
            if answer_option.is_true:
                return i

    @property
    def poll_info(self):
        return {
            "question": self.question,
            "options": [option.answer for option in self.answer_options],
            "correct_option_id": self.correct_answer_num,
            "explanation": self.answer_description,
            "type": "quiz",
            "is_anonymous": False
        }
