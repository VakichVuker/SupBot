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
        'no_pryaniks_current_month': 'Нет пряников за текущий месяц месяц',
        'hello_message': '''Всем привет! 
Меня зовут СУП-bot (Система учета пряников), для начала работы со мной каждому из Вас необходимо перейти ко мне в личку @seoworkSupBot и выбрать свою роль:

- Участник - обычный участник пряничной системы, он может дарить пряники, а также получать их (и пиздюли).
- Big Boss - не участвует в получении пряников, но может выдавать пряники и пиздюли, а также вызывать отображение статистики для всех.
- Manager - не участвует в получении пряников, но может их выдавать. 

После выбора роли владелец бота подтвердит Ваше участие и по команде /start Вы сможете вызывать контекстное меню с Вашим функционалом. 
Всё взаимодействие со мной происходит исключительно в личке, в данную группу я самостоятельно буду отправлять все необходимые уведомления.

Мой код на github - https://github.com/VakichVuker/SupBot''',
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
                text += f"- {pryanik[3]} от {pryanik[1]} за \"{pryanik[0]}\" \n"
            else:
                pizdyl_count += 1
                pizdyl_text += f"- {pryanik[3]} от {pryanik[1]} за \"{pryanik[0]}\" \n"
        return text if pizdyl_count == 0 else text + pizdyl_text

    @staticmethod
    def get_pryanik_description_for_group(pryanik):
        return f'''
@{pryanik['donor']['username']}, {pryanik['donor']['fullname']} кинул {'пиздюлем ' if pryanik['is_pizdyl'] else 'пряником '} в @{pryanik['receiver']['username']}, {pryanik['receiver']['fullname']}
{'Пиздюль ' if pryanik['is_pizdyl'] else 'Пряник '} получен за {'уебанство в' if pryanik['is_pizdyl'] else 'следующие заслуги'}:
{pryanik['description']}
        '''

    @staticmethod
    def get_pryanik_description_for_receiver(pryanik):
        return f'''
В вас кинул(-а) пряником @{pryanik['donor']['username']}, {pryanik['donor']['fullname']}. 
Может тоже хочешь кинуть в кого то пряником? /start 
'''

    @staticmethod
    def get_contester_month_stat(pryaniks: list):
        all_pryaniks = [pryanik for pryanik in pryaniks if bool(pryanik[4]) == 0]
        text = f"📈 В текущем месяце у вас {len(all_pryaniks)} пряников \nА вот список всех полученных в этом месяце пряников:\n"

        for pryanik in pryaniks:
            if not bool(pryanik[4]):
                text += f"- {pryanik[3]} от {pryanik[1]} за \"{pryanik[0]}\" \n"
        return text
