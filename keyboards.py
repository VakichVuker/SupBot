from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

all_roles = (
    {
        'name': 'contester',
        'button_text': 'Участник'
    },
    {
        'name': 'big_boss',
        'button_text': 'Big Boss'
    },
    {
        'name': 'manager',
        'button_text': 'Менеджер'
    }
)


def get_choose_contester_keyboard(all_contesters, keyboard_type='pryanik'):
    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    for contester in all_contesters:
        new_button = InlineKeyboardButton(contester['fullname'], callback_data=f'give_{keyboard_type}:{contester["id"]}')
        inline_kb_full.add(new_button)
    return inline_kb_full


def get_roles_choice_keyboard():
    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    for role in all_roles:
        new_button = InlineKeyboardButton(role['button_text'], callback_data=f'set_role{role["name"]}')
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
