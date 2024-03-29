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

        receiver_data = bot_config.sqlite_db.get_user_data_by_username(receiver_username)

        if receiver_data is None:
            await message.reply(
                bot_config.message_helper.MESSAGES['receiver_not_exist'].format(receiver_username)
            )
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
            await message.reply(
                bot_config.message_helper.MESSAGES['multipryanik_success'].format(
                    receiver_username,
                    count,
                    reason
                )
            )
            return
        await message.reply(bot_config.message_helper.MESSAGES['multipryanik_wrong'])
