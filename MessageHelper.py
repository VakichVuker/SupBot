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
        'write_pryanik_description': 'Опиши за что ты кинул пряник, отправив обычное сообщение или отправив фото-мем с описанием (в формате jpeg или png):',
        'write_pizdyl_description': 'Опиши за что ты выдал пиздюль, отправив обычное сообщение или отправив фото-мем с описанием (в формате jpeg или png):',
        'role_approve': 'user_id = {}, fullname = {}, username=@{}\n хочет стать ролью {}.',
        'success_approve': 'Тебе одобрили доступ, можешь пользоваться ботом, для вывода меня нажми /start',
        'failed_approve': 'Тебя тут не ждут',
        'softdelete_delete': 'Пользователь был удален',
        'softdelete_restore': 'Пользователь был восстановлен',
        'multipryanik_limit': 'Может ты цифрой ошибся? Давай не больше чем по 10',
        'multipryanik_format': 'Формат команды следующий: \n@{} @username_получателя 10 любое описание пряников',

        'no_data_previous_month': 'Нет данных за прошлый месяц',
        'no_data_current_month': 'Нет данных за текущий месяц',
        'no_pryaniks_current_month': 'Нет пряников за текущий месяц месяц',
        'write_nickname': 'Напишите свой новый ник (до 20 символов включая форматирование):',
        'incorrect_input': 'Некорректный ввод, длина ника должна достигать максимум 30 символов, введите ник ещё раз:',
        'nickname_change_accept': 'Ник успешно изменен, теперь все будут видеть вас как: {}',
        'multipryanik_wrong': 'Что-то пошло не так при сохранении пряников, обратитесь к моему создателю',
        'multipryanik_success': 'Отправлено @{} {} пряников за: {}',
        'multipizdul_success': 'Отправлено @{} {} пиздюлей за: {}',
    }

    MONTH_RU_STRING = {
        1: 'январь',
        2: 'февраль',
        3: 'март',
        4: 'апрель',
        5: 'март',
        6: 'июнь',
        7: 'июль',
        8: 'август',
        9: 'сентябрь',
        10: 'октябрь',
        11: 'ноябрь',
        12: 'декабрь',
    }

    def __init__(self, bot_name):
        self.bot_name = bot_name
        self.MESSAGES['go_private'] = f'Пойдем ты покажешь в кого и что кинуть мне в личке\n@{bot_name}'

    def say_hello(self):
        return f'''Всем привет! 
Меня зовут СУП-bot (Система учета пряников), для начала работы со мной каждому из Вас необходимо перейти ко мне в личку @{self.bot_name} и выбрать свою роль:

- Участник - обычный участник пряничной системы, он может дарить пряники, а также получать их (и пиздюли).
- Big Boss - не участвует в получении пряников, но может выдавать пряники и пиздюли, а также единственный кто может отображать статистику для всех.
- Manager - не участвует в получении пряников, но может их выдавать. 

Также у всех есть возможность менять себе ник в рамках пряничной.

После выбора роли владелец бота подтвердит твое участие и по команде /start ты сможете вызывать контекстное меню со своим функционалом. 
Всё взаимодействие со мной происходит в основном в личке, в данную группу я самостоятельно буду отправлять все необходимые уведомления.

Но также у меня есть команды для чата, в котором я нахожусь:
(для работы этого функционала у меня в группе, куда меня добавили, должна быть роль админа, владелец проверь)\n
-команда для быстрой отправки нескольких пряников прямо в чате группы
 <code>@{self.bot_name} @username 10 описание того за что пользователь получил пряник</code>
--@username - имя получателя пряников, указанное в тг
--10 - кол-во пряников (min 1 max 10)
--все что написано после кол-ва будет добавлено как описание к прянику 

Мой код на github - https://github.com/VakichVuker/SupBot'''

    def say_update(self):
        return f'''
Всем привет! Кто-то решил немного заебаться на выходных и выкатил обновление для бота. Теперь можно:
*новое 
-просто факт

* каждый участник может посмотреть в чате бота сколько пряников, кому и за что он отправил в этом месяце. 

* каждый из участников может менять ник, отображаемый в кнопках и в описании пряников. (любой пришедший Vasya_Fucker_228 сможет стать обычным человеком без доебов лазанья в бд-шку). Также в никах можно использовать базовые эмоджи.  

* добавил возможность мультипряничной выдачи, с помощью команды в чате, куда добавлен бот.  
<code>@{self.bot_name} @username 10 описание того за что пользователь получил пряник</code>
--@username - имя получателя пряников, указанное в тг
--10 - кол-во пряников (min 1 max 10)
--все что написано после кол-ва будет добавлено как описание к прянику 

* изменил отображение статистики, поменял местами кнопочки для БигБоссов, а то интерфейсы этих телеграммов интуитивно не удобно листать вниз. Теперь красивые сообщения о победителях точно будут залетать к нам в общий чатик. 

* добавил возможность софт_делитить участников пряничной для БигБоссов, так что если Vasya_Fucker_228 вовремя не поменяет ник, то его можно за это подзабанить на время (ну а также можно просто удалять участников без доебов и лазанья в бд). 

- порефачил код бота, но все ещё без слез не взглянешь
- порефачил FSM для бота
- подредачил сообщения на менее официальный стиль текста, а также сделал более красивые отображения в разных сообщениях
 '''

    def get_winners(self, all_stat, month):
        start_message = f"Полная статистика за {self.MONTH_RU_STRING[month]}:\n(кол-во очков, из пряников вычтены пиздюли, если они есть)\n\n"
        return start_message + '\n'.join([
            f"{contester_stat['place']}. {contester_stat['fullname']}, @{contester_stat['username']} - {contester_stat['count']}"
            for contester_stat in all_stat
        ])

    def top1_get_final_winner(self, winner, pryaniks, month):
        text = f"👑 В пряничной за {self.MONTH_RU_STRING[month]} победил(-а)\n<b>{winner['fullname']}</b>, @{winner['username']}. \n\n"
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
    def message_with_place(winner, pryaniks):
        place_emoji = {
            1: '🥇',
            2: '🥈',
            3: '🥉',
        }

        pizdyl_text = "\nНо также им были получены и пиздюли:\n"
        pryanik_text = ""

        pizdyl_count = 0
        pryanik_count = 0
        for pryanik in pryaniks:
            if not bool(pryanik[4]):
                pryanik_count += 1
                pryanik_text += f"- {pryanik[3]} от {pryanik[1]} за \"{pryanik[0]}\" \n"
            else:
                pizdyl_count += 1
                pizdyl_text += f"- {pryanik[3]} от {pryanik[1]} за \"{pryanik[0]}\" \n"

        start_message = f"{place_emoji[winner['place']]} <b>{winner['place']} место </b>\n<b>{winner['fullname']}</b>, @{winner['username']} набрал(-a) {pryanik_count} очков пряничной.\n\n"

        return start_message + pryanik_text if pizdyl_count == 0 else start_message + pryanik_text + pizdyl_text

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

