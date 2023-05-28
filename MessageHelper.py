class MessageHelper:
    MESSAGES = {
        'start': 'Привет, {} выбери кем ты будешь в пряничной системе:',
        'throw_pryanik': 'Вы кинули пряник.',
        'throw_pizdyl': 'Вы выдали пиздюль.',
        'description_added': 'Описание успешно добавлено, спасибо за работу!',
        'contester_exist': 'Мы с тобой уже знакомы, держи меню',
        'contester_not_exist': 'Введи /start для нашего знакомства, а там посмотрим. ',
        'role_choose': 'Вы выбрали роль, ожидайте подтверждения от владельца бота. После этого Вы сможете пользоваться функционалом.',
        'choose_receiver': 'Выберите счастливчика',
        'write_pryanik_description': 'Опишите за что вы кинули пряник, отправив обычное сообщение:',
        'write_pizdyl_description': 'Опишите за что вы выдали пиздюль, отправив обычное сообщение:',
        'role_approve': 'user_id = {}, fullname = {}, username=@{}\n хочет стать ролью {}.',
        'success_approve': 'Вам одобрили доступ, можете пользоваться ботом',
        'failed_approve': 'Вас тут не ждут',
        'go_private': 'Пойдем ты покажешь в кого и что кинуть мне в личке, @seoworkSupBot',
        'no_data_previous_month': 'Нет данных за прошлый месяц',
        'no_data_current_month': 'Нет данных за текущий месяц месяц',
    }

    @staticmethod
    def get_winners(all_stat):
        return '\n'.join([
            f"{contester_stat['place']}. {contester_stat['fullname']} - {contester_stat['count']} шт."
            for contester_stat in all_stat
        ])

    @staticmethod
    def get_final_winner(winner, pryaniks):
        text = f"👑 В пряничной за прошлый месяц победил {winner['fullname']}. \n А вот список всех полученных за месяц пряников: \n"
        pizdyl_text = "Но также им были получены и пиздюли:\n"
        pizdyl_count = 0
        for pryanik in pryaniks:
            if not bool(pryanik[4]):
                text += f"- {pryanik[3]} от @{pryanik[1]} за \"{pryanik[0]}\" \n"
            else:
                pizdyl_count += 1
                pizdyl_text += f"- {pryanik[3]} от @{pryanik[1]} за \"{pryanik[0]}\" \n"
        return text if pizdyl_count == 0 else text + pizdyl_text

    @staticmethod
    def get_pryanik_description(pryanik):
        return f'''
@{pryanik['donor']['username']}, {pryanik['donor']['fullname']} кинул {'пиздюлем ' if pryanik['is_pizdyl'] else 'пряником '} в @{pryanik['receiver']['username']}, {pryanik['receiver']['fullname']}
{'Пиздюль ' if pryanik['is_pizdyl'] else 'Пряник '} получен за следующие заслуги:
{pryanik['description']}
        '''
