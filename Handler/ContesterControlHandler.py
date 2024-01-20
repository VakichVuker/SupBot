from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity


def initialize_handlers(bot_config: BotConfigEntity):
    check_some_shit_handler(bot_config)


def check_some_shit_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_delete_contester['title']
    )
    async def check_new_message(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        if not user_data:
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_not_exist']
            )
            return
        if int(user_data['is_confirmed']) != 1 or user_data['role'] != 'big_boss':
            return



        await bot_config.bot.send_message(message.from_user.id, text='Эта хуйня работает')
