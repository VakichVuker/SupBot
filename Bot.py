import os

from aiogram import executor

from ConfigEntities.BotConfig import BotConfigEntity
from Handler import AdminMessageHandler, StartHandler, StatisticHandler, PryanikThrowHandler, ContesterControlHandler


if __name__ == "__main__":
    bot_config = BotConfigEntity(root_path=os.path.dirname(os.path.abspath(__file__)))

    StartHandler.initialize_handlers(bot_config=bot_config)
    AdminMessageHandler.initialize_handlers(bot_config=bot_config)
    PryanikThrowHandler.initialize_handlers(bot_config=bot_config)
    StatisticHandler.initialize_handlers(bot_config=bot_config)
    ContesterControlHandler.initialize_handlers(bot_config=bot_config)

    executor.start_polling(bot_config.dp)
