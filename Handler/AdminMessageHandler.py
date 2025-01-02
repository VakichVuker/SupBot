import datetime as datetime
from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity


def initialize_handlers(bot_config: BotConfigEntity):
    check_some_shit_handler(bot_config)
    say_hello_handler(bot_config)
    say_update_handler(bot_config)
    current_month_stat_admin(bot_config)
    previous_month_stat_admin(bot_config)


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


def current_month_stat_admin(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message:
        message.text == 'че там у хохлов'
        and str(message.from_user.id) == str(bot_config.config['TelegramData']['owner_chat_id'])
    )
    async def check_stat(message: types.Message):
        current_month = datetime.datetime.now().strftime('%m')
        current_year = datetime.datetime.now().strftime('%Y')
        data = bot_config.sqlite_db.get_stat(current_month, current_year)
        if data:
            await message.reply(
                bot_config.message_helper.get_winners(
                    data,
                    int(current_month)
                )
            )
        else:
            await message.reply(bot_config.message_helper.MESSAGES['no_data_current_month'])

def previous_month_stat_admin(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message:
        message.text == 'че там было у хохлов'
        and str(message.from_user.id) == str(bot_config.config['TelegramData']['owner_chat_id'])
    )
    async def check_stat_prev(message: types.Message):
        today = datetime.date.today().replace(day=1)
        previous_month = today - datetime.timedelta(days=1)
        data = bot_config.sqlite_db.get_stat(
            month=previous_month.strftime('%m'),
            year=previous_month.strftime('%Y')
        )
        if data:
            await message.reply(
                bot_config.message_helper.get_winners(
                    data,
                    int(previous_month.strftime('%m')))
            )
        else:
            await message.reply(bot_config.message_helper.MESSAGES['no_data_previous_month'])