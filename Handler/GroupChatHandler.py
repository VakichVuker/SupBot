from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity
from aiogram.dispatcher import filters
import datetime as datetime


def initialize_handlers(bot_config: BotConfigEntity):
    pryanik_multiadd_handler(bot_config)


def pryanik_multiadd_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        filters.Text(startswith='@' + bot_config.message_helper.bot_name)
    )
    async def multipryanik(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)

        if not user_data:
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_not_exist']
            )
            return

        if user_data['is_confirmed'] != 1:
            await message.reply('С тобой я не общаюсь')
            return

        data = message.text.split(' ')
        count = data[2]

        reason = ' ' .join(data[3:])
        receiver_username = str(data[1]).replace('@', '')
        try:
            count = int(count)
        except Exception as e:
            await message.reply(
                bot_config.message_helper.MESSAGES['multipryanik_format'].format(bot_config.message_helper.bot_name)
            )
            return

        if count == 0:
            await message.reply('Умно, но нет')

        if count < 0 and user_data['role'] != 'big_boss' and user_data['role'] != 'ultimate_contester' and user_data['role'] != 'ultimate_manager':
            await message.reply('Ты не можешь кидать пиздюли')
            return

        receiver_data = bot_config.sqlite_db.get_user_data_by_username(receiver_username)

        if receiver_data is None:
            await message.reply(
                bot_config.message_helper.MESSAGES['receiver_not_exist'].format(receiver_username)
            )
            return

        if receiver_data['id'] == message.from_user.id:
            if count > 0:
                message_text = 'Держи шире карман'
            else:
                message_text = 'Суецыд не выход, падумай'
            await message.reply(message_text)
            return

        receiver_full_data = bot_config.sqlite_db.get_auth_data(receiver_data['id'])

        if receiver_full_data['role'] != 'contester' and receiver_full_data['role'] != 'ultimate_contester':
            await message.reply('Этому человеку нельзя отправить пряники')
            return

        if count > 10:
            await message.reply(
                bot_config.message_helper.MESSAGES['multipryanik_limit']
            )
            return

        is_added = bot_config.sqlite_db.add_multipryanic(
            description=reason,
            donor_id=message.from_user.id,
            reciever_id=receiver_data['id'],
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
            count=count
        )
        if is_added:
            if count > 0:
                message_type = 'multipryanik_success'
            else:
                message_type = 'multipizdul_success'

            await message.reply(
               bot_config.message_helper.MESSAGES[message_type].format(
                    receiver_username,
                    abs(count),
                    reason
                )
            )
            return
        await message.reply(bot_config.message_helper.MESSAGES['multipryanik_wrong'])
