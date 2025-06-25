#!/bin/bash

# Этот скрипт запускается после деплоя для инициализации шедулера гороскопов

echo "==================================================="
echo "Инициализация шедулера гороскопов"
echo "==================================================="

# Проверяем наличие необходимых пакетов
pip install schedule

# Создаем systemd service для запуска шедулера
if [ -d "/etc/systemd/system" ]; then
    echo "Настраиваем systemd сервис для шедулера гороскопов..."
    
    cat > /tmp/horoscope-scheduler.service << EOF
[Unit]
Description=Horoscope Scheduler Service
After=network.target

[Service]
User=root
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python $(pwd)/schedule_horoscopes.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Копируем файл сервиса
    sudo cp /tmp/horoscope-scheduler.service /etc/systemd/system/
    
    # Обновляем, включаем и запускаем сервис
    sudo systemctl daemon-reload
    sudo systemctl enable horoscope-scheduler.service
    sudo systemctl start horoscope-scheduler.service
    
    echo "Сервис шедулера настроен и запущен"
else
    echo "Systemd не найден, запускаем шедулер через nohup..."
    nohup python schedule_horoscopes.py > horoscope_scheduler_output.log 2>&1 &
    echo "Шедулер запущен в фоновом режиме (PID: $!)"
fi

echo "==================================================="
echo "Инициализация шедулера завершена"
echo "==================================================="
