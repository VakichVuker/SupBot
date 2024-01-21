from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity
from aiogram.dispatcher import filters
import datetime as datetime


def initialize_handlers(bot_config: BotConfigEntity):
    pryanik_multiadd_handler(bot_config)


def pryanik_multiadd_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        filters.Text(startswith='@suppryaniktest_bot')
    )
    async def send_welcome(message: types.Message):
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
        receiver = str(data[1]).replace('@', '')
        try:
            count = int(count)
        except Exception as e:
            await message.reply(
                bot_config.message_helper.MESSAGES['multipryanik_format']
            )
            return

        receiver_data = bot_config.sqlite_db.get_user_data_by_username(receiver)

        if receiver_data is None:
            await message.reply(
                bot_config.message_helper.MESSAGES['receiver_not_exist']
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
            await message.reply('Отправлено @' + receiver + ' ' + str(count) + ' пряников по причине: ' + reason)
            return
        await message.reply('Что-то пошло не так, вероятно получатель сменил свой @username, если он хочет получить сразу много пряников пусть прожмет /start у меня в чате')
