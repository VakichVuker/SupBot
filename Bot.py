import datetime as datetime
import configparser
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import Keyboards as CustomKeyboards
from MessageHelper import MessageHelper
from Utils import States
from Sqlite import SqlLiteHelper

config = configparser.ConfigParser()
config.read("settings.ini")

bot = Bot(token=config['Settings']['token'])
dp = Dispatcher(bot=bot, storage=MemoryStorage())
sqlite_db = SqlLiteHelper(db_file=config['Settings']['db_name'])
message_helper = MessageHelper


@dp.message_handler(lambda message: message.text == "Чекирование")
async def start_message(message: types.Message):
    user_data = sqlite_db.get_auth_data(message.from_user.id)
    if not user_data:
        await message.reply(message_helper.MESSAGES['contester_not_exist'])
        return
    keyboard = CustomKeyboards.get_standart_keyboard_by_role(user_data['role'])
    await message.reply(message_helper.MESSAGES['contester_exist'], reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if message.chat.type != 'private':
        await message.reply(message_helper.MESSAGES['go_private'])
        return
    user_full_name = message.from_user.full_name

    if sqlite_db.add_contester(message.from_user.id, user_full_name, message.from_user.username):
        keyboard = CustomKeyboards.get_roles_choice_keyboard()
        await message.reply(message_helper.MESSAGES['start'].format(user_full_name), reply_markup=keyboard)
    else:
        user_data = sqlite_db.get_auth_data(message.from_user.id)
        await message.reply(
            message_helper.MESSAGES['contester_exist'],
            reply_markup=CustomKeyboards.get_standart_keyboard_by_role(user_data['role'])
        )


@dp.message_handler(state=States.WRITING_DESCRIPTION)
async def add_description(message: types.Message):
    if message.chat.type != 'private':
        await message.reply(message_helper.MESSAGES['go_private'])
        return
    updated_id = sqlite_db.add_description_to_last_record(message.from_user.id, message.text)
    message_text = message_helper.get_pryanik_description(sqlite_db.get_pryanik(updated_id))
    await bot.send_message(
        config['TelegramData']['group_chat_id'],
        text=message_text
    )

    state = dp.current_state(user=message.from_user.id)
    user_data = sqlite_db.get_auth_data(message.from_user.id)

    await state.reset_state()
    await message.reply(message_helper.MESSAGES['description_added'],
                        reply=False,
                        reply_markup=CustomKeyboards.get_standart_keyboard_by_role(user_data['role']))


@dp.message_handler(lambda message: message.text == CustomKeyboards.command_send_pryanik['title'])
async def pryanik_send_message(message: types.Message):
    if message.chat.type != 'private':
        await message.reply(message_helper.MESSAGES['go_private'])
        return
    user_list = sqlite_db.get_all_contesters_except_one(message.from_user.id)
    keyboard = CustomKeyboards.get_choose_contester_keyboard(user_list)
    await message.reply(message_helper.MESSAGES['choose_receiver'], reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == CustomKeyboards.command_send_pizdyl['title'])
async def pizdyl_send_message(message: types.Message):
    user_data = sqlite_db.get_auth_data(message.from_user.id)
    if not user_data:
        await message.reply(message_helper.MESSAGES['contester_not_exist'])
        return
    if message.chat.type != 'private' or int(user_data['is_confirmed']) != 1 or user_data['role'] != 'big_boss':
        await message.reply(message_helper.MESSAGES['go_private'])
        return
    user_list = sqlite_db.get_all_contesters_except_one(message.from_user.id)
    keyboard = CustomKeyboards.get_choose_contester_keyboard(user_list, 'pizdyl')
    await message.reply(message_helper.MESSAGES['choose_receiver'], reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == CustomKeyboards.command_get_stat_current_month['title'])
async def get_stat_message(message: types.Message):
    user_data = sqlite_db.get_auth_data(message.from_user.id)
    if not user_data:
        return
    if message.chat.type != 'private' or user_data['role'] != 'big_boss' or user_data['is_confirmed'] != 1:
        return
    current_month = datetime.datetime.now().strftime('%m')
    data = sqlite_db.get_stat(current_month)
    if data:
        await message.reply(message_helper.get_winners(data))
    else:
        await message.reply(message_helper.MESSAGES['no_data_current_month'])


@dp.message_handler(lambda message: message.text == CustomKeyboards.command_get_stat_previous_month['title'])
async def get_stat_message(message: types.Message):
    user_data = sqlite_db.get_auth_data(message.from_user.id)
    if not user_data:
        return
    if message.chat.type != 'private' or user_data['role'] != 'big_boss' or user_data['is_confirmed'] != 1:
        return
    today = datetime.date.today().replace(day=1)
    previous_month = today - datetime.timedelta(days=1)
    data = sqlite_db.get_stat(previous_month.strftime('%m'))
    if data:
        await message.reply(message_helper.get_winners(data))
    else:
        await message.reply(message_helper.MESSAGES['no_data_previous_month'])


@dp.message_handler(lambda message: message.text == CustomKeyboards.command_show_winner_to_all['title'])
async def send_winner_data_to_all(message: types.Message):
    user_data = sqlite_db.get_auth_data(message.from_user.id)
    if not user_data:
        return
    if message.chat.type != 'private' or user_data['role'] != 'big_boss' or user_data['is_confirmed'] != 1:
        return
    today = datetime.date.today().replace(day=1)
    previous_month = today - datetime.timedelta(days=1)
    data = sqlite_db.get_stat(previous_month.strftime('%m'))
    if data:
        winner = data[0]
        winner_pryaniks = sqlite_db.get_all_pryanik_by_contester(winner['contester_id'], previous_month.strftime('%m'))
    else:
        await message.reply(message_helper.MESSAGES['no_data_previous_month'])
        return

    await bot.send_message(
        config['TelegramData']['group_chat_id'],
        text=message_helper.get_final_winner(winner, winner_pryaniks)
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('set_role'))
async def role_authorization_callback(callback_query: types.CallbackQuery):
    sender_id = callback_query.from_user.id
    full_name = callback_query.from_user.full_name
    username = callback_query.from_user.username

    callback_data = str(callback_query.data[8:])
    sqlite_db.update_role(callback_data, sender_id)

    await bot.send_message(
        config['TelegramData']['owner_chat_id'],
        text=message_helper.MESSAGES['role_approve'].format(sender_id, full_name, username, callback_data),
        reply_markup=CustomKeyboards.get_approve_keyboard(sender_id)
    )
    await bot.send_message(callback_query.from_user.id, message_helper.MESSAGES['role_choose'])
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('approve'))
async def approve_role_callback(callback_query: types.CallbackQuery):
    callback_data = str(callback_query.data[7:]).split(':')
    contester_id = callback_data[1]
    if callback_data[0] == 'accept':
        sqlite_db.confirm_contester(contester_id)
        user_data = sqlite_db.get_auth_data(contester_id)
        await bot.send_message(
            contester_id,
            message_helper.MESSAGES['success_approve'],
            reply_markup=CustomKeyboards.get_standart_keyboard_by_role(user_data['role'])
        )
    else:
        await bot.send_message(contester_id, message_helper.MESSAGES['failed_approve'])
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('give_'))
async def store_button_callback(callback_query: types.CallbackQuery):
    sender_id = callback_query.from_user.id
    data = str(callback_query.data[5:]).split(':')
    record_type = data[0]
    receiver_id = int(data[1])

    sqlite_db.add_record('no_data', sender_id, receiver_id, datetime.datetime.now().strftime('%Y-%m-%d'), record_type)
    state = dp.current_state(user=callback_query.from_user.id)

    await state.set_state(States.all()[0])
    await bot.send_message(callback_query.from_user.id, message_helper.MESSAGES[f'throw_{record_type}'])
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, message_helper.MESSAGES[f'write_{record_type}_description'])


if __name__ == "__main__":
    executor.start_polling(dp)
