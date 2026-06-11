# Architecture

WorldCupDNA's backend is a **modular monolith** built on FastAPI. One deployable
app, but the code is split into self-contained domain modules so multiple
developers can work in parallel and a module could later be extracted into its
own service with minimal churn.

## Layout

```
worldcupdna-backend/
├── app/
│   ├── main.py                 # app factory; wires every module router under /api/v1
│   ├── models_registry.py      # imports all ORM models so create_all sees them
│   │
│   ├── core/                   # cross-cutting infrastructure
│   │   ├── config.py           # pydantic-settings; all env vars live here
│   │   ├── database.py         # engine, SessionLocal, Base, get_db()
│   │   ├── security.py         # bcrypt hashing + JWT (access/refresh)
│   │   ├── dependencies.py     # get_current_user / _admin / _optional_user
│   │   └── cache.py            # in-process TTL cache (protects API rate limits)
│   │
│   ├── integrations/           # third-party API clients (no business logic)
│   │   ├── football_data/      # football-data.org v4 client + normalizer
│   │   └── statsbomb/          # StatsBomb open-data + paid client
│   │
│   ├── shared/                 # tiny shared helpers (id generation, …)
│   │
│   └── modules/                # one folder per domain
│       ├── users/   auth/   matches/   predictions/   leaderboard/
│       ├── venues/  notifications/  players/  stats/  payments/  admin/
│       └── <module>/
│           ├── models.py        # SQLAlchemy ORM (omitted where a module owns no table)
│           ├── schemas.py       # Pydantic request/response models
│           ├── service.py       # business logic — the only place that mutates state
│           └── router.py        # thin HTTP layer; delegates to service
│
├── scripts/                    # operational scripts (run with `python -m scripts.x`)
│   ├── seed_venues.py          # seed Nairobi watch-party venues
│   ├── sync_matches.py         # pull WC fixtures/results from football-data.org
│   ├── migrate.py              # idempotent ALTER TABLE for existing databases
│   └── create_admin.py         # promote/create an admin user
│
├── docs/                       # this folder
├── requirements.txt            # pinned deps (UTF-8)
├── runtime.txt                 # python-3.11.0 (Render)
└── .env.example                # documented env template
```

## Module anatomy

Every module follows the same contract:

| File         | Responsibility                                                        |
|--------------|-----------------------------------------------------------------------|
| `models.py`  | Database tables (SQLAlchemy). Some modules have none (e.g. leaderboard derives from users). |
| `schemas.py` | Pydantic models — the validated shape of input and output.            |
| `service.py` | All business logic and DB access. Routers never touch the DB directly except through `get_db`. |
| `router.py`  | FastAPI routes. Parse/validate → call service → return schema.        |

**Rule of thumb:** logic goes in `service.py`; routers stay thin. This keeps
endpoints testable and lets services call each other (e.g. `admin` reuses
`predictions.service.score_match`).

## Request lifecycle

1. `main.create_app()` builds the app, adds CORS, includes every module router
   under `settings.API_PREFIX` (`/api/v1`).
2. A request hits a router → dependencies resolve (`get_db`, auth).
3. The router calls into its `service`, which does the work and returns ORM
   objects or dicts.
4. FastAPI serializes the result through the route's `response_model`.

## Data sources

- **Fixtures, results, standings, scorers** → football-data.org (free tier),
  synced into our `matches` table and cached. See
  [football-data-integration.md](./football-data-integration.md).
- **Advanced analytics (xG, shot maps)** → StatsBomb. See
  [statsbomb-integration.md](./statsbomb-integration.md).
- **Player photos** → TheSportsDB (free, no key).
- **Everything else** (users, predictions, venues, …) → our own Postgres (Neon).

## Auth

Stateless JWT. `create_access_token` / `create_refresh_token` embed a `type`
claim; `get_current_user` accepts only `access` tokens and checks `is_active`.
Admin routes depend on `get_current_admin`. Passwords are hashed with bcrypt
directly (no passlib — it breaks against bcrypt ≥ 4.1).

## Adding a new module

1. `mkdir app/modules/<name>` with `__init__.py`, `models.py`, `schemas.py`,
   `service.py`, `router.py`.
2. If it owns tables, add its models to `app/models_registry.py`.
3. Import and include its router in `app/main.py`.

That's it — no other wiring needed.
