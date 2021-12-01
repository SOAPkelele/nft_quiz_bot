from dataclasses import dataclass


@dataclass
class StoredUser:
    telegram_id: int
    username: str
    full_name: str
    lang: str
