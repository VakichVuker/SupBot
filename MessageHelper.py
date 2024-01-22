class MessageHelper:
    MESSAGES = {
        'start': 'Привет, {} выбери кем ты будешь в пряничной системе:',
        'throw_pryanik': 'Ты кинул(-а) пряник.',
        'throw_pizdyl': 'Ты выдал пиздюль.',
        'description_added': 'Описание успешно добавлено, спасибо за работу!',
        'contester_exist': 'Мы с тобой уже знакомы, держи меню',
        'contester_not_exist': 'Введи /start для нашего знакомства, а там посмотрим. ',
        'receiver_not_exist': 'Не найден получатель по нику @{}, вероятно получатель сменил свой @username со времен последнего общения со мной, если он хочет получить сразу много пряников пусть прожмет /start у меня в чате, после повторите ввод команды',
        'role_choose': 'Ты выбрал роль, ожидай подтверждения от владельца бота. После этого ты сможешь пользоваться функционалом.',
        'choose_receiver': 'Выбери счастливчика',
        'choose_delete': 'Выбери кого будем удалять',
        'choose_restore': 'Выбери кого восстановим',
        'write_pryanik_description': 'Опиши за что ты кинул пряник, отправив обычное сообщение:',
        'write_pizdyl_description': 'Опиши за что ты выдал пиздюль, отправив обычное сообщение:',
        'role_approve': 'user_id = {}, fullname = {}, username=@{}\n хочет стать ролью {}.',
        'success_approve': 'Тебе одобрили доступ, можешь пользоваться ботом, для вывода меня нажми /start',
        'failed_approve': 'Тебя тут не ждут',
        'softdelete_delete': 'Пользователь был удален',
        'softdelete_restore': 'Пользователь был восстановлен',
        'multipryanik_limit': 'Может ты цифрой ошибся? Давай не больше чем по 10',
        'multipryanik_format': 'Формат команды следующий: \n@{} @username_получателя 10 любое описание пряников',

        'no_data_previous_month': 'Нет данных за прошлый месяц',
        'no_data_current_month': 'Нет данных за текущий месяц месяц',
        'no_pryaniks_current_month': 'Нет пряников за текущий месяц месяц',
        'write_nickname': 'Напишите свой новый ник (до 20 символов включая форматирование):',
        'incorrect_input': 'Некорректный ввод, длина ника должна достигать максимум 30 символов, введите ник ещё раз:',
        'nickname_change_accept': 'Ник успешно изменен, теперь все будут видеть вас как: {}',
        'multipryanik_wrong': 'Что-то пошло не так при сохранении пряников, обратитесь к моему создателю',
        'multipryanik_success': 'Отправлено @{} {} пряников за заслуги: {}',
    }

    def __init__(self, bot_name):
        self.bot_name = bot_name
        self.MESSAGES['go_private'] = f'Пойдем ты покажешь в кого и что кинуть мне в личке\n@{bot_name}'

    def say_hello(self):
        return f'''Всем привет! 
Меня зовут СУП-bot (Система учета пряников), для начала работы со мной каждому из Вас необходимо перейти ко мне в личку @{self.bot_name} и выбрать свою роль:

- Участник - обычный участник пряничной системы, он может дарить пряники, а также получать их (и пиздюли).
- Big Boss - не участвует в получении пряников, но может выдавать пряники и пиздюли, а также вызывать отображение статистики для всех.
- Manager - не участвует в получении пряников, но может их выдавать. 

После выбора роли владелец бота подтвердит твое участие и по команде /start ты сможете вызывать контекстное меню со своим функционалом. 
Всё взаимодействие со мной происходит исключительно в личке, в данную группу я самостоятельно буду отправлять все необходимые уведомления.

Мой код на github - https://github.com/VakichVuker/SupBot'''

    @staticmethod
    def get_winners(all_stat):
        return '\n'.join([
            f"{contester_stat['place']}. {contester_stat['fullname']} - {contester_stat['count']} шт."
            for contester_stat in all_stat
        ])

    @staticmethod
    def get_final_winner(winner, pryaniks):
        text = f"👑 В пряничной за прошлый месяц победил(-а) {winner['fullname']}. \n"
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
В тебя кинул(-а) пряником @{pryanik['donor']['username']}, {pryanik['donor']['fullname']}. 
Может тоже хочешь кинуть в кого-то пряником? /start 
'''

    @staticmethod
    def get_contester_month_stat(pryaniks: list):
        all_pryaniks = [pryanik for pryanik in pryaniks if bool(pryanik[4]) == 0]
        text = f"📈 В этом месяце у вас {len(all_pryaniks)} пряников \n"

        for pryanik in pryaniks:
            if not bool(pryanik[4]):
                text += f"- {pryanik[3]} от {pryanik[1]} за \"{pryanik[0]}\" \n"
        return text

    @staticmethod
    def get_sended_stat(pryaniks: list):
        result = ''
        all_pryaniks = [pryanik for pryanik in pryaniks if bool(pryanik[4]) == 0]
        for pryanik in all_pryaniks:
            result += f"- {pryanik[3]} для {pryanik[1]} за \"{pryanik[0]}\"\n"

        all_pizdyl = [pryanik for pryanik in pryaniks if bool(pryanik[4]) == 1]
        if len(all_pizdyl) != 0:
            result += f"\n☠️ В этом месяце вы раздали {len(all_pizdyl)} пиздюлей \n"
            for pizdyl in all_pizdyl:
                result += f"- {pizdyl[3]} для {pizdyl[1]} за \"{pizdyl[0]}\"\n"

        return result
