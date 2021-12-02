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
