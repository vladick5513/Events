# Event Booking API

**Event Booking API** — это RESTful API для системы бронирования мероприятий. Оно позволяет пользователям регистрироваться, аутентифицироваться, управлять мероприятиями и просматривать доступные события.  

---

## Функциональность

### 1. Пользователи
- Регистрация новых пользователей с именем, электронной почтой и паролем.
- Аутентификация с использованием JWT.
- Защита маршрутов, требующих авторизации, через токены доступа.

### 2. Мероприятия
- CRUD-операции для управления мероприятиями (создание, чтение, обновление и удаление).
- Просмотр списка всех мероприятий и детальной информации о каждом из них.
- Фильтрация мероприятий по названию и дате.

### 3. Безопасность и обработка ошибок
- Все защищенные маршруты требуют действующего JWT-токена.
- Обработка ошибок с понятными сообщениями, включая валидацию входных данных и статусы HTTP.

---
### 4. Запуск приложения
1. Запустите сервер разработки:


- uvicorn app.main:app --reload

После запуска API будет доступно по адресу: http://127.0.0.1:8000.

2. Документация API
- Для удобного взаимодействия с API вы можете использовать автоматически сгенерированную документацию:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc
### Тестирование


Приложение поставляется с набором тестов для основных бизнес-логик, таких как регистрация, аутентификация и управление мероприятиями.


#### Запустите тесты:
```bash
pytest
```
### Архитектура
- **FastAPI**: фреймворк для построения RESTful API.
- **SQLAlchemy**: ORM для взаимодействия с PostgreSQL.
- **PostgreSQL**: база данных для хранения пользователей и мероприятий.
- **Pydantic**: для валидации данных.
- **Alembic**: управление миграциями базы данных.
- **Pytest**: тестирование.

