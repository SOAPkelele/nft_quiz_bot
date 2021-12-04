from dataclasses import dataclass
from typing import List

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from environs import Env
from pytz import UTC, timezone


@dataclass
class TgBot:
    token: str


@dataclass
class DB:
    user: str
    password: str
    database: str
    host: str


@dataclass
class FSMStorageType:
    type: str

    @property
    def storage(self):
        if self.type == "redis":
            return RedisStorage2()  # host="redis"
        else:
            return MemoryStorage()


@dataclass
class NotificationChats:
    broadcast_chat_id: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DB
    fsm_storage: FSMStorageType
    admins: List[int]
    notification_chat_id: int
    default_timezone: UTC
    skip_updates: bool


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
        ),
        db=DB(
            host=env.str("POSTGRES_IP"),
            user=env.str("POSTGRES_USER"),
            database=env.str("POSTGRES_DB"),
            password=env.str("POSTGRES_PASSWORD")
        ),
        fsm_storage=FSMStorageType(
            type=env.str("FSM_STORAGE")
        ),
        admins=env.list("ADMINS"),
        notification_chat_id=env.int("BROADCAST_CHAT"),
        default_timezone=timezone('Europe/Moscow'),
        skip_updates=env.bool("SKIP_UPDATES")
    )
