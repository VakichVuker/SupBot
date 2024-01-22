from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity


def initialize_handlers(bot_config: BotConfigEntity):
    start_handler(bot_config)
    authorize_handlers(bot_config)


def start_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        if message.chat.type != 'private':
            await message.reply(bot_config.message_helper.MESSAGES['go_private'])
            return
        user_full_name = message.from_user.full_name

        if bot_config.sqlite_db.add_contester(message.from_user.id, user_full_name, message.from_user.username):
            keyboard = bot_config.keyboard_helper.get_roles_choice_keyboard()
            await message.reply(bot_config.message_helper.MESSAGES['start'].format(user_full_name), reply_markup=keyboard)
        else:
            user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
            if message.from_user.username != user_data['username']:
                bot_config.sqlite_db.update_username_for_existing_user(message.from_user.id, message.from_user.username)
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_exist'],
                reply_markup=bot_config.keyboard_helper.get_standart_keyboard_by_role(user_data['role'])
            )


def authorize_handlers(bot_config: BotConfigEntity):
    @bot_config.dp.callback_query_handler(lambda c: c.data and c.data.startswith('set_role'))
    async def role_authorization_callback(callback_query: types.CallbackQuery):
        sender_id = callback_query.from_user.id
        full_name = callback_query.from_user.full_name
        username = callback_query.from_user.username

        callback_data = str(callback_query.data[8:])
        bot_config.sqlite_db.update_role(callback_data, sender_id)

        await bot_config.bot.send_message(
            chat_id=bot_config.config['TelegramData']['owner_chat_id'],
            text=bot_config.message_helper.MESSAGES['role_approve'].format(sender_id, full_name, username, callback_data),
            reply_markup=bot_config.keyboard_helper.get_approve_keyboard(sender_id)
        )
        await bot_config.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=bot_config.message_helper.MESSAGES['role_choose']
        )
        await bot_config.bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id
        )

    @bot_config.dp.callback_query_handler(lambda c: c.data and c.data.startswith('approve'))
    async def approve_role_callback(callback_query: types.CallbackQuery):
        callback_data = str(callback_query.data[7:]).split(':')
        contester_id = callback_data[1]

        if callback_data[0] == 'accept':
            bot_config.sqlite_db.confirm_contester(contester_id)
            user_data = bot_config.sqlite_db.get_auth_data(contester_id)
            await bot_config.bot.send_message(
                contester_id,
                bot_config.message_helper.MESSAGES['success_approve'],
                reply_markup=bot_config.keyboard_helper.get_standart_keyboard_by_role(user_data['role'])
            )
        else:
            await bot_config.bot.send_message(
                contester_id,
                bot_config.message_helper.MESSAGES['failed_approve']
            )

        await bot_config.bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id
        )