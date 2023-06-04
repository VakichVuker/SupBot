from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

command_send_pryanik = {
    'title': 'Отправить пряник',
    'command': '/pryanik_send',
}
command_send_pizdyl = {
    'title': 'Отправить пиздюль',
    'command': '/pizdyl_send',
}
command_show_self_contester_stat = {
    'title': 'Мои пряники в этом месяце',
    'command': '/show_self_contester_stat',
}
command_get_stat_current_month = {
    'title': 'Показать статистику на текущий месяц',
    'command': '/get_stat_current_month',
}
command_get_stat_previous_month = {
    'title': 'Показать статистику на предыдущий месяц',
    'command': '/get_stat_previous_month',
}
command_show_winner_to_all = {
    'title': 'Отправить в общий чат информацию о победителе за прошлый месяц',
    'command': '/show_winner_to_all',
}

all_roles = {
    'contester': {
        'button_text': 'Участник',
        'enabled_buttons': (
            command_send_pryanik,
            command_show_self_contester_stat,
        )
    },
    'big_boss': {
        'button_text': 'Big Boss',
        'enabled_buttons': (
            command_send_pryanik,
            command_send_pizdyl,
            command_get_stat_current_month,
            command_get_stat_previous_month,
            command_show_winner_to_all
        )
    },
    'manager': {
        'button_text': 'Менеджер',
        'enabled_buttons': (command_send_pryanik,)
    }
}


def get_choose_contester_keyboard(all_contesters, keyboard_type='pryanik'):
    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    for contester in all_contesters:
        new_button = InlineKeyboardButton(contester['fullname'],
                                          callback_data=f'give_{keyboard_type}:{contester["id"]}')
        inline_kb_full.add(new_button)
    return inline_kb_full


def get_roles_choice_keyboard():
    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    for role_name, role_settings in all_roles.items():
        new_button = InlineKeyboardButton(role_settings['button_text'], callback_data=f'set_role{role_name}')
        inline_kb_full.add(new_button)
    return inline_kb_full


def get_approve_keyboard(user_id):
    data = (
        {
            'button_text': 'Подтвердить',
            'callback_data': 'accept'
        },
        {
            'button_text': 'Отказать',
            'callback_data': 'decline'
        }
    )
    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    for button_data in data:
        new_button = InlineKeyboardButton(
            button_data['button_text'],
            callback_data=f'approve{button_data["callback_data"]}:{user_id}'
        )
        inline_kb_full.add(new_button)
    return inline_kb_full


def get_standart_keyboard_by_role(role):
    keyboard_list = all_roles[role]
    keyboard = ReplyKeyboardMarkup()
    print()
    for button in keyboard_list['enabled_buttons']:
        button = KeyboardButton(button['title'])
        keyboard.add(button)
    return keyboard
