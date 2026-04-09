# DimatechTask1 — Payment REST API

Асинхронное REST API для управления пользователями, счетами и платежами.

**Стек:** FastAPI, PostgreSQL, SQLAlchemy (async), Alembic, Docker Compose

***

## Тестовые учётные данные

**Пользователь:** `user@test.com` / `user123`

**Администратор:** `admin@test.com` / `admin123`

***

## Запуск с Docker Compose

```bash
git clone <url репозитория>
cd DimatechTask1

cp .env.example .env

docker compose up --build
```

Приложение запустится на **http://localhost:8000**

Swagger UI: **http://localhost:8000/docs**

> Миграции применяются автоматически при старте контейнера.

***

## Запуск без Docker Compose

**Требования:** Python 3.11+, PostgreSQL

```bash
git clone <url репозитория>
cd DimatechTask1

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install -r requirements.txt

cp .env.example .env
```

Открыть `core/config.py` и заполнить:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
PAYMENT_SECRET_KEY=gfdmhghif38yrf9ew0jkf32
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

```bash
python -m alembic upgrade head

python -m uvicorn app.main:app --reload
```

Приложение запустится на **http://127.0.0.1:8000**

Swagger UI: **http://127.0.0.1:8000/docs**
