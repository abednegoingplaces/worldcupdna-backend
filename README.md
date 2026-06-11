# WorldCupDNA Backend API

A FIFA World Cup 2026 fan identity & prediction platform. Fans build a "Football
DNA" profile, predict scores for real fixtures, climb a global leaderboard,
track live standings, and find watch-party venues.

- **Live API:** https://worldcupdna-backend.onrender.com
- **Interactive docs:** https://worldcupdna-backend.onrender.com/docs

## Stack

- **FastAPI** (modular monolith) on Python 3.11
- **PostgreSQL** (Neon)
- **football-data.org** for real WC 2026 fixtures, scores, standings, scorers
- **StatsBomb** for advanced analytics (xG, shot maps)
- Deployed on **Render**

## Architecture

A modular monolith — each domain lives under `app/modules/<name>/` with its own
`models`, `schemas`, `service`, and `router`. See
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

```
app/
  core/         config, database, security, dependencies, cache
  integrations/ football_data, statsbomb
  modules/      users auth matches predictions leaderboard venues
                notifications players stats payments admin
scripts/        seed_venues  sync_matches  migrate  create_admin
docs/           ARCHITECTURE  API  football-data-integration  statsbomb-integration
```

## Quickstart

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # then fill in DATABASE_URL, SECRET_KEY, FOOTBALL_API_KEY

# (existing database) apply additive column migrations
python -m scripts.migrate

# seed Nairobi watch-party venues
python -m scripts.seed_venues

# pull real World Cup fixtures into the DB
python -m scripts.sync_matches

# run
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs.

## Configuration

All settings come from environment variables (`.env` in dev). See
[.env.example](.env.example) for the full list. Key ones:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Neon Postgres connection string |
| `SECRET_KEY` | JWT signing secret (generate a strong one) |
| `FOOTBALL_API_KEY` | football-data.org free-tier key |
| `CORS_ORIGINS` | comma-separated origins, or `*` |
| `STATSBOMB_USERNAME/PASSWORD` | optional — paid StatsBomb access |

## Scripts

| Command | What it does |
|---------|--------------|
| `python -m scripts.migrate` | idempotent `ALTER TABLE` for existing DBs |
| `python -m scripts.seed_venues` | seed watch-party venues |
| `python -m scripts.sync_matches` | sync WC fixtures/results from football-data.org (run on a schedule) |
| `python -m scripts.create_admin <email>` | create/promote an admin |

## Documentation

- [API reference](docs/API.md) — every endpoint
- [Architecture](docs/ARCHITECTURE.md) — how the modular monolith fits together
- [football-data.org integration](docs/football-data-integration.md) — all free-tier functionality
- [StatsBomb integration](docs/statsbomb-integration.md) — xG / advanced stats

## Deployment (Render)

The `Procfile` runs migrations on release and starts the server:

```
release: python -m scripts.migrate
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

`runtime.txt` pins Python 3.11.0. Set the env vars from `.env.example` in the
Render dashboard. Schedule `python -m scripts.sync_matches` as a Render cron job
during the tournament to keep scores fresh.
