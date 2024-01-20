# SupBot
Система Учета Пряников (и пиздюлей) для отдела разработки. 

# Настройки на стороне телеграмма
Бот не требует большого перечня команд, весь функционал реализован на всплывающих клавиатурах-кнопках. Имеет смысл только добавить команду /start для того чтобы пользователь мог "перепризвать" клавиатуру, если она у него пропадет. 

# Deploy на Linux сервер
* изменить файл .settins.ini на settings.ini и вставить в него соответствующие данные. </br>
* apt update
* apt upgrade -y
* apt install python3
* apt install python3-pip
* pip3 install aiogram 2.25.2

- также могут возникнуть проблемы с пакетом sqlite3, стабильно работает на версии 3.35.0

* cd /etc/systemd/system
* nano name_bot.service

*  В файл вставьте следующие строки
```
[Unit]
Description=Pryanichniy bot dlya otdela
After=network.target
[Service]
ExecStart=/usr/bin/python3 /route/to/Bot.py
[Install]
WantedBy=multi-user.target
```
*  systemctl enable name_bot</br>
*  systemctl start name_bot</br>
#### Теперь при запуске сервера будет работать автозапуск скрипта. 
