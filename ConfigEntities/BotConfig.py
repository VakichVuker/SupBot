import configparser
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Keyboards import KeyboardHelper
from PictureStorage import PictureStorage
from MemeStorage import MemeStorage
from MessageHelper import MessageHelper
from Sqlite import SqlLiteHelper


class BotConfigEntity:
    def __init__(self, root_path):
        self.config = configparser.ConfigParser()
        self.config.read(root_path + "/settings.ini", 'utf_8_sig')

        self.bot = Bot(token=self.config['Settings']['token'])
        self.dp = Dispatcher(bot=self.bot, storage=MemoryStorage())

        db_filepath = root_path + '/' + self.config['Settings']['db_name'] + '.sqlite'
        self.sqlite_db = SqlLiteHelper(db_file=db_filepath)

        self.picture_storage = PictureStorage(root_path)
        self.meme_storage = MemeStorage(root_path)
        self.message_helper = MessageHelper(self.config['TelegramData']['bot_username'])

        self.keyboard_helper = KeyboardHelper()
