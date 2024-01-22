from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity


def initialize_handlers(bot_config: BotConfigEntity):
    check_some_shit_handler(bot_config)
    say_hello_handler(bot_config)
    say_update_handler(bot_config)


def check_some_shit_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message:
        message.text == 'check work'
        and str(message.from_user.id) == str(bot_config.config['TelegramData']['owner_chat_id'])
    )
    async def check_new_message(message: types.Message):
        await bot_config.bot.send_message(message.from_user.id, text='Я работаю')


def say_hello_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message:
        message.text == 'say hello'
        and str(message.from_user.id) == str(bot_config.config['TelegramData']['owner_chat_id'])
    )
    async def hello_group_message(message: types.Message):
        await bot_config.bot.send_message(
            bot_config.config['TelegramData']['group_chat_id'],
            text=bot_config.message_helper.say_hello(),
            parse_mode=types.ParseMode.HTML
        )


def say_update_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message:
        message.text == 'say update'
        and str(message.from_user.id) == str(bot_config.config['TelegramData']['owner_chat_id'])
    )
    async def update_group_message(message: types.Message):
        await bot_config.bot.send_message(
            bot_config.config['TelegramData']['group_chat_id'],
            text=bot_config.message_helper.say_update(),
            parse_mode=types.ParseMode.HTML
        )