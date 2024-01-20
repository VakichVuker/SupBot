from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    writing_description = State()
    change_nickname = State()
