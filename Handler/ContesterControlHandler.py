from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity
from Utils import States


def initialize_handlers(bot_config: BotConfigEntity):
    change_nickname_handler(bot_config)
    nickname_handler(bot_config)
    delete_contester_handler(bot_config)
    restore_contester_handler(bot_config)
    softdelete_result_save_handler(bot_config)


def change_nickname_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_contester_change_fullname['title']
    )
    async def change_nickname(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)

        if not user_data:
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_not_exist']
            )
            return

        if user_data['is_confirmed'] != 1:
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


def nickname_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(state=States.change_nickname)
    async def change_fullname(message: types.Message):
        if message.chat.type != 'private':
            await message.reply(bot_config.message_helper.MESSAGES['go_private'])
            return

        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)

        if not user_data:
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_not_exist']
            )
            return
        if user_data['is_confirmed'] != 1:
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


def delete_contester_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_delete_contester['title']
    )
    async def soft_delete_contester(message: types.Message):
        if message.chat.type != 'private':
            await message.reply(bot_config.message_helper.MESSAGES['go_private'])
            return

        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)

        if not user_data:
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_not_exist']
            )
            return
        if user_data['role'] != 'big_boss' or user_data['is_confirmed'] != 1:
            return

        user_list = bot_config.sqlite_db.get_all_users_except_one(message.from_user.id)
        keyboard = bot_config.keyboard_helper.get_choose_contester_keyboard(
            user_list,
            keyboard_type='softdelete',
            row_type='delete'
        )

        await message.reply(
            bot_config.message_helper.MESSAGES['choose_delete'],
            reply_markup=keyboard
        )


def restore_contester_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_restore_contester['title']
    )
    async def soft_delete_contester(message: types.Message):
        if message.chat.type != 'private':
            await message.reply(bot_config.message_helper.MESSAGES['go_private'])
            return

        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)

        if not user_data:
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_not_exist']
            )
            return
        if user_data['role'] != 'big_boss' or user_data['is_confirmed'] != 1:
            return

        user_list = bot_config.sqlite_db.get_all_soft_delete_users(message.from_user.id)
        keyboard = bot_config.keyboard_helper.get_choose_contester_keyboard(
            user_list,
            keyboard_type='softdelete',
            row_type='restore'
        )
        await message.reply(
            bot_config.message_helper.MESSAGES['choose_restore'],
            reply_markup=keyboard
        )


def softdelete_result_save_handler(bot_config: BotConfigEntity):
    @bot_config.dp.callback_query_handler(lambda c: c.data and c.data.startswith('softdelete_'))
    async def store_button_callback(callback_query: types.CallbackQuery):
        data = str(callback_query.data[11:]).split(':')
        action_type = data[0]
        user_id = int(data[1])

        bot_config.sqlite_db.soft_delete_user(user_id, action_type)

        await bot_config.bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id
        )
        await bot_config.bot.send_message(
            callback_query.from_user.id,
            bot_config.message_helper.MESSAGES[f'softdelete_{action_type}']
        )
