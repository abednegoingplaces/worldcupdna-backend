# football-data.org integration

The free tier is the **primary live data source** for WorldCupDNA. It carries
real FIFA World Cup 2026 data (competition id **2000**): all 104 fixtures, 12
groups, live scores, standings and top scorers.

- Base URL: `https://api.football-data.org/v4`
- Auth header: `X-Auth-Token: <FOOTBALL_API_KEY>`
- **Rate limit: 10 requests/minute** on the free tier — every call in
  `app/integrations/football_data/client.py` is wrapped in a short TTL cache
  (`app/core/cache.py`) to stay under it.

## How we use it

| Concern | Endpoint | Where |
|---------|----------|-------|
| Sync all WC fixtures into our DB | `GET /competitions/2000/matches` | `matches.service.sync_world_cup` |
| Today / recent / upcoming / live | served from our synced `matches` table | `matches.service` |
| Group standings (live) | `GET /competitions/2000/standings` | `matches.service.standings` |
| Top scorers | `GET /competitions/2000/scorers` | `players.service.top_scorers` |

We **sync** matches into Postgres rather than proxying every read so that (a)
predictions can foreign-key to a stable match id and (b) reads don't burn the
rate limit. `scripts/sync_matches.py` refreshes scores/statuses; run it on a
schedule during the tournament.

## Full list of free-tier functionality (what you *can* integrate)

The free tier exposes 13 competitions. For each, these endpoints are available:

### Competitions
- `GET /competitions` — list all competitions you can access.
- `GET /competitions/{id}` — competition detail (current season, dates).

### Matches / fixtures
- `GET /competitions/{id}/matches` — all matches for a competition. Filters:
  - `dateFrom` / `dateTo` (YYYY-MM-DD) — **powers "today's" and "recent" matches**
  - `status` — `SCHEDULED`, `TIMED`, `IN_PLAY`, `PAUSED`, `FINISHED`, `POSTPONED`, `SUSPENDED`, `CANCELLED`
  - `stage` — e.g. `GROUP_STAGE`, `LAST_16`, `QUARTER_FINALS`, `SEMI_FINALS`, `FINAL`
  - `group` — e.g. `GROUP_A`
  - `matchday` — integer
- `GET /matches/{id}` — single match detail (lineups/goals where provided).
- `GET /matches?ids=...` or date filters — cross-competition match listing.

### Standings
- `GET /competitions/{id}/standings` — group/league tables (TOTAL/HOME/AWAY).

### Scorers
- `GET /competitions/{id}/scorers?limit=N` — top scorers (goals, assists,
  penalties where available).

### Teams
- `GET /competitions/{id}/teams` — teams in a competition (with crests).
- `GET /teams/{id}` — team detail + squad.
- `GET /teams/{id}/matches` — a team's matches (filter by status/date/limit).

### Areas (countries/confederations)
- `GET /areas` and `GET /areas/{id}` — geographic areas.

## What the free tier does NOT include

- **No expected goals (xG)**, shot-level events, or detailed player match stats.
- No advanced tactical/positional data.

For those, we use **StatsBomb** — see
[statsbomb-integration.md](./statsbomb-integration.md).

## Status normalization

football-data statuses are mapped to our simpler vocabulary in
`integrations/football_data/normalize.py`:

| football-data           | ours        |
|-------------------------|-------------|
| `SCHEDULED`, `TIMED`    | `scheduled` |
| `IN_PLAY`, `PAUSED`     | `live`      |
| `FINISHED`              | `finished`  |
| `POSTPONED`, `SUSPENDED`, `CANCELLED` | passed through lowercased |

## Error handling

The client raises `FootballDataError` on a 429 (rate limit) or non-200. Routers
that proxy live (standings, scorers) translate this into HTTP 502 so the
frontend can show a graceful "live data temporarily unavailable" state. Synced
reads (matches table) keep working regardless.
