class MessageHelper:
    MESSAGES = {
        'start': 'Привет, {} выбери кем ты будешь в пряничной системе:',
        'throw_pryanik': 'Вы кинули пряник.',
        'pryanik_added': 'Пряник успешно добавлен, спасибо за работу!',
        'contester_exist': 'Мы с тобой уже знакомы, держи меню',
        'contester_not_exist': 'Введи /start для нашего знакомства, а там посмотрим. ',
        'role_choose': 'Вы выбрали роль, ожидайте подтверждения от владельца бота. После этого Вы сможете пользоваться функционалом.',
        'choose_receiver': 'Выберите счастливчика',
        'write_description': 'Опишите за что вы кинули пряник, отправив обычное сообщение:',
        'role_approve': 'user_id = {}, fullname = {}, username=@{}\n хочет стать ролью {}.',
        'success_approve': 'Вам одобрили доступ, можете пользоваться ботом',
        'failed_approve': 'Вас тут не ждут',
        'go_private': 'Пойдем ты отдашь мне свои пряники в личке, @seoworkSupBot',
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
        pizdul_text = "Но также им были получены и пиздюли:\n"
        pizdul_count = 0
        for pryanik in pryaniks:
            if not bool(pryanik[4]):
                text += f"- {pryanik[3]} от @{pryanik[1]} за \"{pryanik[0]}\" \n"
            else:
                pizdul_count += 1
                pizdul_text += f"- {pryanik[3]} от @{pryanik[1]} за \"{pryanik[0]}\" \n"
        return text if pizdul_count == 0 else text + pizdul_text

    @staticmethod
    def get_pryanik_description(pryanik):
        return f'''
@{pryanik['donor']['username']}, {pryanik['donor']['fullname']} кинул {'пиздюлем ' if pryanik['is_pizdul'] else 'пряником '} в @{pryanik['receiver']['username']}, {pryanik['receiver']['fullname']}
{'Пиздюль ' if pryanik['is_pizdul'] else 'Пряник '} получен за следующие заслуги:
{pryanik['description']}
        '''
