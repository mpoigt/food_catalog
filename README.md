# Auth Service — «Каталог продуктов»

Сервис аутентификации и авторизации на **FastAPI**, построенный по принципам **чистой архитектуры**
(domain → application → infrastructure → presentation). Часть тестового задания «Каталог продуктов».

## Возможности

- Регистрация и вход (JWT: access/refresh), ротация refresh-токена с blacklist в Redis.
- Три роли: `user` / `advanced` / `admin` (ролевые guard-зависимости FastAPI).
- Администрирование пользователей: создание, смена роли, блокировка, смена пароля, удаление.
- Пароли — `bcrypt` (соль на пользователя). Токены различают тип (access/refresh).
- Блокировка действует немедленно (проверка в БД на каждый запрос), а не по истечении токена.
- Структурное (JSON) логирование ключевых и аудит-событий.

## Стек

FastAPI · SQLAlchemy 2 (async) · Alembic · PostgreSQL · Redis · dependency-injector · PyJWT · bcrypt · Poetry · Docker

## Архитектура

Модульный монолит с общим ядром. Каждый модуль внутри разбит на слои чистой архитектуры:

```
src/
  core/       общее ядро: settings, Base/engine/session, BaseUnitOfWork, logging, exceptions, DI
  auth/       модуль аутентификации/авторизации
  catalog/    модуль каталога продуктов
    domain/          сущности и enum-ы (без внешних зависимостей)
    application/     use-cases, порты (repositories/services/config), DTO, исключения
    infrastructure/  реализации портов: БД (Data Mapper + UnitOfWork), Redis, JWT, bcrypt, config
    presentation/    FastAPI-роутеры, схемы, DI-контейнер, зависимости авторизации
  main.py     композиция: CoreContainer → контейнеры модулей → роутеры
```

Зависимости направлены строго внутрь: `core` не знает о модулях; `domain` ни от чего не зависит,
`application` знает только свои порты, конкретные реализации живут в `infrastructure`/`presentation`.

## Быстрый старт (Docker)

```bash
cp .env.example .env                 # Windows: copy .env.example .env
docker compose up -d --build         # поднимает PostgreSQL + Redis + приложение (миграции накатываются автоматически)
```

- Swagger UI: <http://127.0.0.1:8000/docs>
- PostgreSQL: `localhost:5433` (`postgres` / `postgres` / `auth_db`)

### Первый администратор

Регистрация создаёт роль `user`. Чтобы завести админа, выполните разово:

```bash
docker compose exec auth python -m auth.scripts.seed_admin
```

(или создайте пользователя и вручную выставьте ему `role = 'ADMIN'` в БД).

## Локальная разработка

Все команды выполняются **из корня проекта** (там лежит `.env`).

```bash
poetry install
cp .env.example .env
# нужны запущенные PostgreSQL и Redis (docker compose up -d db redis)
DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/auth_db PYTHONPATH=src poetry run alembic -c src/alembic.ini upgrade head
PYTHONPATH=src poetry run uvicorn main:app --reload
```

## Тесты

Пирамида: `unit` (на фейках, без внешних зависимостей) · `integration` (репозиторий против реального
Postgres) · `e2e` (полный API через httpx, БД реальная, Redis замокан).

```bash
poetry run pytest src/tests/unit                     # быстрые, без БД
poetry run pytest src/tests/integration src/tests/e2e  # нужен запущенный Postgres (docker compose up -d db)
poetry run pytest                                    # всё сразу
```

Тестовая база `test_auth_db` **создаётся автоматически** фикстурами (отдельно от рабочей `auth_db`);
адрес берётся из `TEST_DB_URL`.

## Основные эндпоинты

| Метод | Путь | Доступ | Назначение |
|-------|------|--------|-----------|
| POST | `/auth/register` | публичный | регистрация (роль `user`) |
| POST | `/auth/login` | публичный | вход, возвращает пару токенов |
| POST | `/tokens/refresh` | публичный | ротация по refresh-токену |
| GET | `/users/` | admin | список (пагинация, сортировка) |
| POST | `/users/` | admin | создать пользователя с ролью |
| GET | `/users/{id}` | admin | получить пользователя |
| PATCH | `/users/{id}` | admin | изменить (роль/блокировка/пароль) |
| PATCH | `/users/{id}/delete` | admin | удалить |

Авторизация в Swagger: `POST /auth/login` → скопировать `access_token` → кнопка **Authorize** → `Bearer <token>`.
