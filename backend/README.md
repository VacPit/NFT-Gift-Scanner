# NFT Gift Scanner: Backend

FastAPI + SQLAlchemy 2 + PostgreSQL. Единый backend для веб-приложения, админ-панели и Telegram-бота.

## Запуск

```bash
cp .env.example .env        # заполнить JWT_SECRET и TELEGRAM_BOT_TOKEN
docker compose up --build   # PostgreSQL + миграции + API на :8000
```

Swagger: http://localhost:8000/docs

## Локальная разработка

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
pytest
```

Тесты используют SQLite in-memory и не требуют PostgreSQL.

## Принципы

- Секреты только из переменных окружения; в production значения по умолчанию не принимаются.
- Единый формат ошибок: `{"error": {"code", "message", "details"}}`.
- Токены и initData маскируются в логах.
- Источник данных сканера: `SCANNER_MODE=demo|real`. Демо-данные всегда помечаются.

## Статус этапов

- [x] 1. Каркас: конфиг, БД, Alembic, ошибки, логирование, health, модель User
- [ ] 2. Авторизация Telegram initData, `/api/users/me`, роли
- [ ] 3. Каталог подарков и заявки
- [ ] 4. Предложения и Scanner
- [ ] 5. Matching и уведомления
- [ ] 6. Статистика и события
- [ ] 7. Admin API
- [ ] 8. Документация и API-контракт для фронтенда
