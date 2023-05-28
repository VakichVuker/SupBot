# SupBot
Система учета пряников. 

# Deploy
* изменить файл .settins.ini на settings.ini и вставить в него соответствующие данные. 
Обновить все пакеты, после чего
* pip3 install aiogram

* cd ../../etc/systemd/system
* nano sup_bot.service

*  В файл вставьте следующие строки
```
[Service]
WorkingDirectory=/pathToFolderWithBot
User=root
ExecStart=/usr/bin/python3 bot.py

[Install]
WantedBy=multi-user.target
EOF
```
*  systemctl enable sup_bot</br>
*  systemctl start sup_bot</br>
#### Теперь при запуске сервера будет работать автозапуск скрипта. 
