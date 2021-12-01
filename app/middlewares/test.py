from aiogram.dispatcher.middlewares import BaseMiddleware as Base
from loguru import logger


class MyBase(Base):
    async def trigger(self, action, args):
        """
        Event trigger

        :param action: event name
        :param args: event arguments
        :return:
        """
        if 'update' not in action \
                and 'error' not in action \
                and action.startswith('pre_process'):
            logger.info(args[0])
            return True
