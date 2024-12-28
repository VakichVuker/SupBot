from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardHelper:
    command_send_pryanik = {
        'title': 'Отправить пряник',
        'command': '/pryanik_send',
    }
    command_send_pizdyl = {
        'title': 'Отправить пиздюль',
        'command': '/pizdyl_send',
    }
    command_show_self_received_pryaniks = {
        'title': 'Мои пряники в этом месяце',
        'command': '/show_self_contester_stat',
    }
    command_get_stat_current_month = {
        'title': 'Статистика за текущий месяц',
        'command': '/get_stat_current_month',
    }
    command_get_stat_previous_month = {
        'title': 'Статистика за предыдущий месяц',
        'command': '/get_stat_previous_month',
    }
    command_show_winner_to_all = {
        'title': 'Отправить в общий чат информацию о победителе за текущий месяц 🎄',
        'command': '/show_winner_to_all',
    }
    command_show_self_sended_pryaniks = {
        'title': 'Отправленные мною пряники в этом месяце',
        'command': '/show_sended_pryaniks',
    }
    command_contester_change_fullname = {
        'title': 'Изменить ник, отображаемый остальным в пряничной',
        'command': '/change_nickname',
    }

    # in develop
    command_delete_contester = {
        'title': 'Удалить пользователя из пряничной',
        'command': '/delete_contester',
    }
    command_restore_contester = {
        'title': 'Восстановить пользователя в пряничной',
        'command': '/restore_contester',
    }

    all_roles = {
        'contester': {
            'button_text': 'Участник',
            'enabled_buttons': (
                command_send_pryanik,
                command_show_self_received_pryaniks,
                command_show_self_sended_pryaniks,
                command_contester_change_fullname
            )
        },
        'ultimate_contester': {
            'button_text': 'Участник с привилегиями',
            'enabled_buttons': (
                command_send_pryanik,
                command_send_pizdyl,
                command_show_self_received_pryaniks,
                command_show_self_sended_pryaniks,
                command_contester_change_fullname
            )
        },
        'big_boss': {
            'button_text': 'Big Boss',
            'enabled_buttons': (
                command_send_pryanik,
                command_send_pizdyl,
                command_show_winner_to_all,
                command_get_stat_current_month,
                command_get_stat_previous_month,
                command_show_self_sended_pryaniks,
                command_delete_contester,
                command_restore_contester,
                command_contester_change_fullname
            )
        },
        'manager': {
            'button_text': 'Менеджер',
            'enabled_buttons': (
                command_send_pryanik,
                command_show_self_sended_pryaniks,
                command_contester_change_fullname
            )
        },
        'ultimate_manager': {
            'button_text': 'Менеджер с привилегиями',
            'enabled_buttons': (
                command_send_pryanik,
                command_send_pizdyl,
                command_show_self_sended_pryaniks,
                command_contester_change_fullname
            )
        }
    }

    @staticmethod
    def get_choose_contester_keyboard(all_contesters, keyboard_type='give', row_type='pryanik'):
        inline_kb_full = InlineKeyboardMarkup(row_width=1)
        for contester in all_contesters:
            new_button = InlineKeyboardButton(contester['fullname'],
                                              callback_data=f'{keyboard_type}_{row_type}:{contester["id"]}')
            inline_kb_full.add(new_button)
        return inline_kb_full

    def get_roles_choice_keyboard(self):
        inline_kb_full = InlineKeyboardMarkup(row_width=1)
        for role_name, role_settings in self.all_roles.items():
            new_button = InlineKeyboardButton(role_settings['button_text'], callback_data=f'set_role{role_name}')
            inline_kb_full.add(new_button)
        return inline_kb_full

    @staticmethod
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

    def get_standart_keyboard_by_role(self, role):
        keyboard_list = self.all_roles[role]
        keyboard = ReplyKeyboardMarkup()
        for button in keyboard_list['enabled_buttons']:
            button = KeyboardButton(button['title'])
            keyboard.add(button)
        return keyboard
