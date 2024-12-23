from aiogram import types
from ConfigEntities.BotConfig import BotConfigEntity
from aiogram.types import InputFile
from Utils import States
import datetime as datetime


def initialize_handlers(bot_config: BotConfigEntity):
    pryanik_choose_receiver_handler(bot_config)
    add_pryanik_description(bot_config)
    pyzdul_send_handler(bot_config)
    store_pryanik_handler(bot_config)


def pryanik_choose_receiver_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(lambda message: message.text == bot_config.keyboard_helper.command_send_pryanik['title'])
    async def pryanik_send_message(message: types.Message):
        if message.chat.type != 'private':
            await message.reply(bot_config.message_helper.MESSAGES['go_private'])
            return
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        if not user_data:
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_not_exist']
            )
            return
        if int(user_data['is_confirmed']) != 1:
            await message.reply(
                bot_config.message_helper.MESSAGES['go_private']
            )
            return
        if message.from_user.username != user_data['username']:
            bot_config.sqlite_db.update_username_for_existing_user(message.from_user.id, message.from_user.username)

        user_list = bot_config.sqlite_db.get_all_contesters_except_one(message.from_user.id)
        keyboard = bot_config.keyboard_helper.get_choose_contester_keyboard(user_list)

        await message.reply(bot_config.message_helper.MESSAGES['choose_receiver'], reply_markup=keyboard)


def add_pryanik_description(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(state=States.writing_description, content_types=['photo', 'text'])
    async def add_description(message: types.Message):
        if message.chat.type != 'private':
            await message.reply(bot_config.message_helper.MESSAGES['go_private'])
            return

        meme_filepath = None

        if message.photo:  # Если есть фото
            photo = message.photo[-1]
            file_info = await bot_config.bot.get_file(photo.file_id)
            downloaded_file = await bot_config.bot.download_file(file_info.file_path)
            meme_filepath = bot_config.meme_storage.get_meme_filepath(message.from_user.id)
            # Сохранение файла локально
            with open(meme_filepath, "wb") as f:
                f.write(downloaded_file.read())

            if message.caption is None:
                input_message_text = 'всё описано мемом 🫶'
            else:
                input_message_text = message.caption
        else:
            input_message_text = message.text

        updated_id = bot_config.sqlite_db.add_description_to_last_record(
            message.from_user.id,
            input_message_text,
            meme_filepath
        )

        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        state = bot_config.dp.current_state(user=message.from_user.id)


        updated_row = bot_config.sqlite_db.get_pryanik(updated_id)

        message_text = bot_config.message_helper.get_pryanik_description_for_group(updated_row)

        await state.reset_state()

        # отправка картинки и текста тому, кому подарили пряник
        if int(updated_row['is_pizdyl']) == 0:
            picture_info = bot_config.picture_storage.get_random_pic()

            if meme_filepath is None:
                file_to_send = InputFile(picture_info['path'])
            else:
                file_to_send = InputFile(meme_filepath)

            if picture_info['type'] == bot_config.picture_storage.TYPE_PHOTO:
                await bot_config.bot.send_photo(
                    updated_row['receiver']['id'],
                    # message.from_user.id,             #для теста отправки при отсутствии помощника
                    file_to_send,
                )
            elif picture_info['type'] == bot_config.picture_storage.TYPE_DOCUMENT:
                await bot_config.bot.send_document(
                    updated_row['receiver']['id'],
                    # message.from_user.id,             #для теста отправки при отсутствии помощника
                    file_to_send,
                )
            await bot_config.bot.send_message(
                updated_row['receiver']['id'],
                # message.from_user.id,                 #для теста отправки при отсутствии помощника
                text=bot_config.message_helper.get_pryanik_description_for_receiver(pryanik=updated_row)
            )

        if meme_filepath is not None:
            # отправка информации в общий чат
            await bot_config.bot.send_photo(
                bot_config.config['TelegramData']['group_chat_id'],
                photo=InputFile(meme_filepath),
                caption=message_text
            )
        else:
            # отправка информации в общий чат
            await bot_config.bot.send_message(
                bot_config.config['TelegramData']['group_chat_id'],
                text=message_text
            )

        await message.reply(
            bot_config.message_helper.MESSAGES['description_added'],
            reply=False,
            reply_markup=bot_config.keyboard_helper.get_standart_keyboard_by_role(user_data['role'])
        )


def pyzdul_send_handler(bot_config: BotConfigEntity):
    @bot_config.dp.message_handler(
        lambda message: message.text == bot_config.keyboard_helper.command_send_pizdyl['title']
        and message.chat.type == 'private'
    )
    async def pizdyl_send_message(message: types.Message):
        user_data = bot_config.sqlite_db.get_auth_data(message.from_user.id)
        if not user_data:
            await message.reply(
                bot_config.message_helper.MESSAGES['contester_not_exist']
            )
            return
        if int(user_data['is_confirmed']) != 1 or user_data['role'] != 'big_boss':
            await message.reply(
                bot_config.message_helper.MESSAGES['go_private']
            )
            return
        user_list = bot_config.sqlite_db.get_all_contesters_except_one(message.from_user.id)
        keyboard = bot_config.keyboard_helper.get_choose_contester_keyboard(user_list, row_type='pizdyl')
        await message.reply(
            bot_config.message_helper.MESSAGES['choose_receiver'],
            reply_markup=keyboard
        )


def store_pryanik_handler(bot_config: BotConfigEntity):
    @bot_config.dp.callback_query_handler(lambda c: c.data and c.data.startswith('give_'))
    async def store_button_callback(callback_query: types.CallbackQuery):
        sender_id = callback_query.from_user.id
        data = str(callback_query.data[5:]).split(':')
        record_type = data[0]
        receiver_id = int(data[1])

        bot_config.sqlite_db.add_record(
            'no_data',
            sender_id,
            receiver_id,
            datetime.datetime.now().strftime('%Y-%m-%d'),
            record_type
        )
        state = bot_config.dp.current_state(user=callback_query.from_user.id)
        await state.set_state(
            States.writing_description
        )
        await bot_config.bot.send_message(
            callback_query.from_user.id,
            bot_config.message_helper.MESSAGES[f'throw_{record_type}']
        )
        await bot_config.bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id
        )
        await bot_config.bot.send_message(
            callback_query.from_user.id,
            bot_config.message_helper.MESSAGES[f'write_{record_type}_description'],
            reply_markup=types.ReplyKeyboardRemove()
        )
