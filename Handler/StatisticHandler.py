from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity
import datetime as datetime


def initialize_handlers(bot_config: BotConfigEntity):
    check_contester_self_stat(bot_config)
    get_full_stat_current_month_handler(bot_config)
    get_full_stat_previous_month_handler(bot_config)
    show_winners_handler(bot_config)
    show_sended_pryaniks(bot_config)


def check_contester_self_stat(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_show_self_received_pryaniks['title']
    )
    async def get_contester_stat_message(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        if message.chat.type != 'private':
            await message.reply(bot_config.message_helper.MESSAGES['go_private'])
            return
        if user_data['role'] != 'contester':
            return

        current_date = datetime.datetime.now()
        data_current_month = bot_config.sqlite_db.get_all_pryanik_by_contester(
            contester_id=message.from_user.id,
            month=current_date.strftime('%m'),
            year=current_date.strftime('%Y')
        )

        if data_current_month:
            await message.reply(
                bot_config.message_helper.get_contester_month_stat(data_current_month),
                reply_markup=bot_config.keyboard_helper.get_standart_keyboard_by_role(user_data['role'])
            )
        else:
            await message.reply(
                bot_config.message_helper.MESSAGES['no_pryaniks_current_month'],
                reply_markup=bot_config.keyboard_helper.get_standart_keyboard_by_role(user_data['role'])
            )


def get_full_stat_current_month_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_get_stat_current_month['title']
        and message.chat.type == 'private'
        )
    async def get_stat_message(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        if not user_data:
            return
        if user_data['role'] != 'big_boss' or user_data['is_confirmed'] != 1:
            return
        current_month = datetime.datetime.now().strftime('%m')
        current_year = datetime.datetime.now().strftime('%Y')
        data = bot_config.sqlite_db.get_stat(current_month, current_year)
        if data:
            await message.reply(bot_config.message_helper.get_winners(data))
        else:
            await message.reply(bot_config.message_helper.MESSAGES['no_data_current_month'])


def get_full_stat_previous_month_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_get_stat_previous_month['title']
                        and message.chat.type == 'private'
    )
    async def get_stat_message(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        if not user_data:
            return
        if user_data['role'] != 'big_boss' or user_data['is_confirmed'] != 1:
            return
        today = datetime.date.today().replace(day=1)
        previous_month = today - datetime.timedelta(days=1)
        data = bot_config.sqlite_db.get_stat(
            month=previous_month.strftime('%m'),
            year=previous_month.strftime('%Y')
        )
        if data:
            await message.reply(bot_config.message_helper.get_winners(data))
        else:
            await message.reply(bot_config.message_helper.MESSAGES['no_data_previous_month'])


def show_winners_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_show_winner_to_all['title']
    )
    async def send_winner_data_to_all(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        if not user_data:
            return
        if message.chat.type != 'private' or user_data['role'] != 'big_boss' or user_data['is_confirmed'] != 1:
            return

        previous_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        # previous_month = datetime.datetime.now()          #для тестов, чтобы выбирать за текущий месяц

        data = bot_config.sqlite_db.get_stat(previous_month.strftime('%m'))
        if data:
            winner = data[0]
            winner_pryaniks = bot_config.sqlite_db.get_all_pryanik_by_contester(
                winner['contester_id'],
                previous_month.strftime('%m'),
                previous_month.strftime('%Y')
            )
        else:
            await message.reply(bot_config.message_helper.MESSAGES['no_data_previous_month'])
            return

        await bot_config.bot.send_message(
            bot_config.config['TelegramData']['group_chat_id'],
            text=bot_config.message_helper.get_final_winner(winner, winner_pryaniks)
        )


def show_sended_pryaniks(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_show_self_sended_pryaniks['title']
    )
    async def show_sended_pryaniks(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        if not user_data:
            return
        if message.chat.type != 'private':
            return

        current_date = datetime.datetime.now()

        data_current_month = bot_config.sqlite_db.get_sended_pryaniks_in_this_month(
            contester_id=message.from_user.id,
            month=current_date.strftime('%m'),
            year=current_date.strftime('%Y')
        )

        if data_current_month:
            await message.reply(
                bot_config.message_helper.get_sended_stat(data_current_month),
                reply_markup=bot_config.keyboard_helper.get_standart_keyboard_by_role(user_data['role'])
            )
        else:
            await message.reply(
                bot_config.message_helper.MESSAGES['no_pryaniks_current_month'],
                reply_markup=bot_config.keyboard_helper.get_standart_keyboard_by_role(user_data['role'])
            )
