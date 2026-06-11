# StatsBomb integration

StatsBomb is the source for **advanced analytics** that football-data.org's free
tier does not provide: expected goals (xG), shot maps, full event data and
lineups.

There are two tiers, and our client (`app/integrations/statsbomb/client.py`)
transparently uses whichever is configured.

## 1. Open Data (free, default) — historical

StatsBomb publishes a large free dataset on GitHub:

- Base: `https://raw.githubusercontent.com/statsbomb/open-data/master/data`
- No credentials required.
- **Full event data including `shot.statsbomb_xg`** (real xG per shot).
- Coverage is **historical**: past World Cups, women's internationals, and
  selected league seasons. It is updated periodically by StatsBomb.

### Important limitation

> StatsBomb Open Data does **not** include live FIFA World Cup **2026** data.
> 2026 fixtures/results/standings come from football-data.org. StatsBomb gives
> us deep analytics on *past* tournaments — perfect for a "deep stats" / xG
> explorer feature, fan education, and historical comparison.

### Open-data endpoints we use

| Call | Path | Returns |
|------|------|---------|
| `list_competitions()` | `/competitions.json` | every available competition+season |
| `list_matches(comp, season)` | `/matches/{comp}/{season}.json` | matches for a season |
| `match_events(match)` | `/events/{match}.json` | full event stream |
| `match_lineups(match)` | `/lineups/{match}.json` | both lineups |
| `shot_xg(match)` | derived from events | every shot with its xG, outcome, location |

Exposed to the frontend via the **`/api/v1/stats`** module:

- `GET /stats/source` — reports whether we're on `open-data` or `paid`.
- `GET /stats/competitions`
- `GET /stats/competitions/{competition_id}/seasons/{season_id}/matches`
- `GET /stats/matches/{match_id}/shots` — shot map data (minute, player, team,
  xG, outcome, pitch location) for rendering an xG shot map.

## 2. Paid API (optional) — live / current-season

If you hold a StatsBomb subscription, set credentials and the same service calls
switch to the authenticated API automatically:

```
STATSBOMB_USERNAME=your-username
STATSBOMB_PASSWORD=your-password
```

- Base: `https://data.statsbomb.com/api` (HTTP Basic auth).
- Adds live and current-season coverage with the same rich event/xG model.
- `client.has_paid_access()` returns `True` when both env vars are set; the
  client then prefers the paid endpoints and falls back to open data otherwise.

Paid responses are cached for a short window (120s) to limit load; open-data
responses are cached for an hour (they rarely change).

## How a "deep stats" feature uses this

1. Frontend calls `/stats/source` to label the data ("Historical xG" vs "Live").
2. Lists competitions/seasons from `/stats/competitions`.
3. For a chosen match, `/stats/matches/{id}/shots` returns shots with `xg` and
   `location` → render a shot map and team xG totals.

This cleanly separates "what's happening in WC 2026" (football-data.org) from
"deep analytical context" (StatsBomb), each from the source that actually has
the data.
