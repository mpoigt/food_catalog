# Каталог продуктов

Веб-приложение из тестового задания: каталог товаров с ролевой моделью доступа.
Фронтенд — SPA на **React + TypeScript**, отвечает только за отображение и пользовательские
сценарии. Вся бизнес-логика и работа с БД — на сервере: **FastAPI**, построенный по чистой
архитектуре (domain → application → infrastructure → presentation).

## Стек

**Backend:** FastAPI · SQLAlchemy 2 (async) · Alembic · PostgreSQL · Redis · dependency-injector ·
PyJWT · bcrypt · Poetry
**Frontend:** React 19 · TypeScript · Vite · React Router · CSS-модули
**Инфраструктура:** Docker Compose

## Возможности

- Каталог продуктов с категориями, описанием, ценой и примечаниями.
- Поиск по названию/описанию, фильтр по категории, сортировка и пагинация — всё на сервере.
- Справочник категорий с CRUD; при удалении категории каскадно удаляются её продукты.
- Загрузка изображений продуктов (JPEG/PNG/WEBP, до 5 МБ).
- Аутентификация и авторизация: JWT (access/refresh), ротация refresh-токена с denylist в Redis.
- Три роли (`user` / `advanced` / `admin`) с проверкой прав на каждом эндпоинте.
- Администрирование пользователей: создание, смена роли, блокировка, смена пароля, удаление.
- Пересчёт цены в USD по курсу Нацбанка РБ выполняет **сервер**: при наведении на «*»
  клиент шлёт запрос `GET /products/{id}/price-usd`, сервер идёт в API НБ РБ (курс кэшируется
  в Redis на день) и возвращает готовую цену в долларах. Запрос уходит через кастомный
  debounce-хук — только если курсор задержан на «*», а не просто проведён по таблице.
- Структурное (JSON) логирование ключевых и аудит-событий.

## Роли и права

| Действие | `user` | `advanced` | `admin` |
|---|:---:|:---:|:---:|
| Просмотр каталога и категорий | ✅ | ✅ | ✅ |
| Поле «Примечание специальное» (видеть и задавать) | — | ✅ | ✅ |
| Добавление / изменение продукта | ✅ | ✅ | ✅ |
| Удаление продукта, CRUD категорий | — | ✅ | ✅ |
| Управление пользователями (создание/блокировка/удаление/смена пароля) | — | — | ✅ |

## Архитектура

Модульный монолит с общим ядром. Каждый модуль внутри разбит на слои чистой архитектуры;
зависимости направлены строго внутрь (`domain` ни от чего не зависит, `application` знает только
свои порты, конкретные реализации живут в `infrastructure`/`presentation`).

```
src/
  core/       общее ядро: settings, Base/engine/session, BaseUnitOfWork, logging, exceptions, DI
  auth/       аутентификация/авторизация и управление пользователями
  catalog/    продукты, категории, изображения, курс валют
    domain/          сущности и enum-ы (без внешних зависимостей)
    application/     use-cases, порты (repositories/services/config), DTO, исключения
    infrastructure/  реализации портов: БД (Data Mapper + UnitOfWork), Redis, JWT, bcrypt
    presentation/    FastAPI-роутеры, схемы, DI-контейнер, зависимости авторизации
  main.py     композиция: CoreContainer → контейнеры модулей → роутеры

frontend/
  src/
    api/         тонкий клиент REST (fetch + рефреш токена)
    components/  переиспользуемый UI (Button, Modal, Field, Toast, ...)
    features/    доменные модули (auth, catalog, admin) — контексты, хуки, компоненты
    pages/       страницы под маршруты
    styles/      theme.css (дизайн-токены) + global.css
```

## Быстрый старт (Docker)

Поднимает весь стек: PostgreSQL, Redis, backend (миграции накатываются автоматически) и frontend.

```bash
cp .env.example .env                 # Windows: copy .env.example .env
docker compose up -d --build
```

- Приложение (SPA): <http://localhost:5173>
- Swagger UI: <http://localhost:8000/docs>
- PostgreSQL: `localhost:5433` (`postgres` / `postgres` / `auth_db`), Redis: `localhost:6379`

### Первый администратор

Регистрация всегда создаёт роль `user`. Чтобы завести администратора, выполните разово:

```bash
docker compose exec auth python -m auth.scripts.seed_admin
```

(или создайте пользователя и вручную выставьте ему `role = 'ADMIN'` в БД).

## Локальная разработка

**Backend** (из корня проекта, где лежит `.env`; нужны запущенные PostgreSQL и Redis —
например `docker compose up -d db redis`):

```bash
poetry install
cp .env.example .env
PYTHONPATH=src poetry run alembic -c src/alembic.ini upgrade head
PYTHONPATH=src poetry run uvicorn main:app --reload
```

**Frontend** (из папки `frontend`):

```bash
npm install
npm run dev
```

Vite поднимается на `:5173` и проксирует `/api` и `/media` на backend
(`API_TARGET`, по умолчанию `http://localhost:8000`).

## Тесты

Пирамида: `unit` (на фейках, без внешних зависимостей) · `integration` (репозиторий против
реального Postgres) · `e2e` (полный API через httpx, БД реальная, Redis замокан).

```bash
poetry run pytest src/tests/unit                       # быстрые, без БД
poetry run pytest src/tests/integration src/tests/e2e  # нужен запущенный Postgres
poetry run pytest                                      # всё сразу
```

Тестовая база `test_auth_db` **создаётся автоматически** фикстурами (отдельно от рабочей
`auth_db`); адрес берётся из `TEST_DB_URL`.

Сборка/типизация фронтенда: `cd frontend && npm run build`.

## Основные эндпоинты

| Метод | Путь | Доступ | Назначение |
|-------|------|--------|-----------|
| POST | `/auth/register` | публичный | регистрация (роль `user`) |
| POST | `/auth/login` | публичный | вход, возвращает пару токенов |
| GET | `/auth/me` | авторизованный | текущий пользователь (роль для UI) |
| POST | `/tokens/refresh` | публичный | ротация по refresh-токену |
| GET | `/users/` | admin | список (пагинация, сортировка) |
| POST | `/users/` | admin | создать пользователя с ролью |
| GET · PATCH · DELETE | `/users/{id}` | admin | получить · изменить · удалить безвозвратно |
| GET | `/categories/` · `/categories/{id}` | авторизованный | список · одна категория |
| POST · PATCH · DELETE | `/categories/...` | advanced/admin | CRUD (удаление каскадит продукты) |
| GET | `/products/` | авторизованный | список: поиск, фильтр по категории, сортировка, пагинация |
| GET | `/products/{id}` | авторизованный | один продукт |
| GET | `/products/{id}/price-usd` | авторизованный | цена в USD (пересчёт на сервере по курсу НБ РБ) |
| POST · PATCH | `/products/` · `/products/{id}` | user+ | создать · изменить |
| POST | `/products/{id}/image` | user+ | загрузить изображение |
| DELETE | `/products/{id}` | advanced/admin | удалить |
| GET | `/currency/usd-rate` | авторизованный | курс USD НБ РБ на сегодня (кэш 1 день) |

Авторизация в Swagger: `POST /auth/login` → скопировать `access_token` → кнопка **Authorize** → `Bearer <token>`.

## Заметки по логике

- **Блокировка ≠ удаление.** Блокировка — это `PATCH /users/{id} {"is_blocked": true}` (обратима),
  удаление через `DELETE` необратимо. Блокировка действует немедленно: пользователь проверяется
  в БД на каждый запрос, а не только по истечении токена.
- **Защита от самоблокировки:** админ не может заблокировать, разжаловать или удалить собственную
  учётную запись.
- **Примечание специальное** роль `user` не видит в ответах API и не может задать при
  создании/изменении продукта — правило симметрично на чтение и на запись.
