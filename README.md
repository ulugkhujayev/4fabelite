# Защищенное API-приложение Django

Это защищенное и масштабируемое API-приложение на Django с управлением пользователями и аутентификацией JWT.

## Особенности

- Пользовательская модель с верификацией по email
- Аутентификация с использованием JWT
- Кэширование с использованием Redis
- Полный набор CRUD-операций для пользователей
- Комплексные тесты
- Расширенное логирование
- Защита от CSRF, XSS и SQL-инъекций
- Ограничение частоты запросов (Rate Limiting)
- Строгие политики паролей
- Docker и Docker Compose для легкого развертывания
- Переменные окружения для безопасной конфигурации

## Установка и запуск

1. Клонируйте репозиторий:
   `git clone https://github.com/your-username/secure-api.git`
   `cd secure-api`

2. Создайте файл .env в корневой директории проекта и заполните его необходимыми значениями:
   `SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@db:5432/secure_api_db
REDIS_URL=redis://redis:6379/1
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
SITE_URL=http://localhost:8000`

3. Соберите и запустите Docker-контейнеры:
   `docker-compose up --build`

4. Примените миграции:
   `docker-compose exec web python manage.py migrate`

5. Создайте суперпользователя:
   `docker-compose exec web python manage.py createsuperuser`

Приложение будет доступно по адресу `http://localhost:8000`

## API Endpoints

`

- POST /api/users/: Создать нового пользователя
- GET /api/users/: Получить список всех пользователей (требует аутентификации)
- GET /api/users/{id}/: Получить информацию о конкретном пользователе (требует аутентификации)
- PUT /api/users/{id}/: Обновить информацию о пользователе (требует аутентификации)
- DELETE /api/users/{id}/: Удалить пользователя (требует аутентификации)
- POST /api/token/: Получить JWT токен
- POST /api/token/refresh/: Обновить JWT токен
- POST /api/users/verify-email/: Подтвердить email пользователя
  `

## API Documentation

API documentation is available through Swagger UI and ReDoc:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

You can also get the OpenAPI schema in JSON or YAML format:

- JSON: http://localhost:8000/swagger.json
- YAML: http://localhost:8000/swagger.yaml

These endpoints provide detailed information about all available API endpoints, request/response formats, and authentication requirements.

## Тестирование

Для запуска тестов выполните:
docker-compose exec web pytest

## Мониторинг и логирование

Логи приложения доступны в файле `debug.log` внутри контейнера. Для просмотра логов используйте команду:
docker-compose exec web cat debug.log

## Безопасность

- Используется HTTPS (в продакшене)
- Защита от CSRF-атак
- Защита от XSS-атак
- Защита от SQL-инъекций
- Ограничение частоты запросов
- Строгие политики паролей

## Административный интерфейс

Административный интерфейс доступен по адресу `http://localhost:8000/admin/`. Используйте учетные данные суперпользователя для входа.
