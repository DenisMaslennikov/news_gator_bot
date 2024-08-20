# Асинхронный бот уведомления о новостях.

Требования:
Установленный docker https://www.docker.com/

1) Клонировать репозиторий локально. ```git clone https://github.com/DenisMaslennikov/news_gator_bot.git```
2) Настроить переменные окружения в файле /config/.env используя в качестве шаблона .env.template в той же директории
3) Запуск с использованием make.
   1) Установить make 
      1) Инструкция для windows https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows
   2) Запустить докер контейнеры ```make start```
4) Запуск без использования make
   1) ```docker compose up --build```

На данный момент в качестве источника новостей поддерживается:
Яндекс Новости
