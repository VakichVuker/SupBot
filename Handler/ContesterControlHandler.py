from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity
from Utils import States


def initialize_handlers(bot_config: BotConfigEntity):
    change_nickname_handler(bot_config)
    change_nickname(bot_config)


def change_nickname_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_contester_change_fullname['title']
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

        await bot_config.bot.send_message(
            message.from_user.id,
            bot_config.message_helper.MESSAGES[f'write_nickname'],
            reply_markup=types.ReplyKeyboardRemove()
        )
        state = bot_config.dp.current_state(user=message.from_user.id)
        await state.set_state(
            States.change_nickname
        )


def change_nickname(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(state=States.change_nickname)
    async def change_fullname(message: types.Message):
        if message.chat.type != 'private':
            await message.reply(bot_config.message_helper.MESSAGES['go_private'])
            return

        if len(message.text) > 31:
            await message.reply(bot_config.message_helper.MESSAGES['incorrect_input'])
            return

        if bot_config.sqlite_db.change_user_fullname(message.from_user.id, message.text):
            state = bot_config.dp.current_state(user=message.from_user.id)
            await state.reset_state()
            await message.reply(bot_config.message_helper.MESSAGES['nickname_change_accept'].format(message.text))
        else:
            await message.reply(bot_config.message_helper.MESSAGES['incorrect_input'])
        return
