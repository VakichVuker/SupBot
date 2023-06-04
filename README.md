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
* pip3 install aiogram

* cd ../../etc/systemd/system
* nano sup_bot.service

*  В файл вставьте следующие строки
```
[Service]
WorkingDirectory=/pathToFolderWithBot
User=root
ExecStart=/usr/bin/python3 Bot.py

[Install]
WantedBy=multi-user.target
EOF
```
*  systemctl enable sup_bot</br>
*  systemctl start sup_bot</br>
#### Теперь при запуске сервера будет работать автозапуск скрипта. 
