И так, для запуска этого замечательного проекта - вам нужно выполнитьследующую инструкцию:)
- Настроить виртуальное окружение
  ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
- Установить зависимости проекта
    ```bash
    pip install -r requirements.txt
    ```
- Установить необходимые драйверы, если их нет:
  ```bash
  sudo apt-get update
  sudo apt install rabbitmq-server
  ```
- Запустить контейнер с базой данных
    ```bash
  docker compose up --build -d
    ```
- Запустить сервис базы данных
    ```bash
  python3 db.py
    ```
- Запустить сервис парсинга
    ```bash
  python3 parser.py
    ```