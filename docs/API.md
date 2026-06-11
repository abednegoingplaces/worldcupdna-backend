# API reference

Base URL: `/api/v1`. Interactive docs are always available at `/docs` (Swagger)
and `/redoc`.

Auth: send `Authorization: Bearer <access_token>` for protected routes. Tokens
come from `/auth/register` and `/auth/login`.

Legend: 🔓 public · 🔑 authenticated · 🛡️ admin only

## Meta
| Method | Path | Notes |
|--------|------|-------|
| GET | `/` | 🔓 service banner |
| GET | `/health` | 🔓 health check |

## Auth — `/auth`
| Method | Path | Notes |
|--------|------|-------|
| POST | `/auth/register` | 🔓 create account (email, username, password + optional DNA: favorite_team, tactical_style, rivalry_level) → tokens |
| POST | `/auth/login` | 🔓 email + password → tokens |
| POST | `/auth/refresh` | 🔓 refresh token → new access token |
| POST | `/auth/logout` | 🔑 client discards tokens (stateless) |
| POST | `/auth/verify-email` | 🔓 confirm email with token |
| POST | `/auth/password-reset/request` | 🔓 request reset token |
| POST | `/auth/password-reset/confirm` | 🔓 set new password |
| GET | `/auth/google` · `/auth/google/callback` | 🔓 OAuth stubs |

## Users — `/users`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/users/me` | 🔑 current profile (email, DNA, points) |
| PATCH | `/users/me` | 🔑 update profile |
| DELETE | `/users/me` | 🔑 delete account |
| PUT | `/users/me/interests` | 🔑 update DNA (team/style/rivalry) |
| GET | `/users/search?q=` | 🔓 search users |
| GET | `/users/{username}` | 🔓 public profile |

## Matches — `/matches`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/matches/?stage=&status=&group=&matchday=` | 🔓 list/filter fixtures |
| GET | `/matches/today` | 🔓 today's matches |
| GET | `/matches/recent?days=3` | 🔓 recently finished |
| GET | `/matches/upcoming?limit=12` | 🔓 next fixtures |
| GET | `/matches/live` | 🔓 in-play matches |
| GET | `/matches/standings` | 🔓 live group tables (football-data) |
| GET | `/matches/{match_id}` | 🔓 single match |

## Predictions — `/predictions`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/predictions/me` | 🔑 my predictions |
| POST | `/predictions/` | 🔑 create/update a score prediction (locked once match starts) |
| PATCH | `/predictions/{id}` | 🔑 edit before kickoff |
| DELETE | `/predictions/{id}` | 🔑 remove before kickoff |
| POST | `/predictions/score/{match_id}` | 🛡️ settle a finished match |

Scoring: exact scoreline = **3 pts**, correct outcome = **1 pt**, else 0.

## Leaderboard — `/leaderboard`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/leaderboard/?limit=100` | 🔓 global ranking; includes `me` row when authenticated |

## Venues — `/venues`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/venues/?city=&county=&country=&lat=&lng=&radius_km=` | 🔓 watch-party venues; returns `{venues, total}`, with `distance_km` when lat/lng given |
| POST | `/venues/submit` | 🔓 submit a venue for review |
| GET | `/venues/{venue_id}` | 🔓 venue detail |

## Notifications — `/notifications`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/notifications/` | 🔑 list + unread count |
| POST | `/notifications/{id}/read` | 🔑 mark one read |
| POST | `/notifications/read-all` | 🔑 mark all read |

## Players — `/players`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/players/scorers?limit=20` | 🔓 top scorers (football-data) |
| GET | `/players/photo/{player_name}` | 🔓 headshot (TheSportsDB) |

## Stats (StatsBomb) — `/stats`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/stats/source` | 🔓 reports `open-data` vs `paid` |
| GET | `/stats/competitions` | 🔓 available competitions/seasons |
| GET | `/stats/competitions/{competition_id}/seasons/{season_id}/matches` | 🔓 matches |
| GET | `/stats/matches/{match_id}/shots` | 🔓 shot map with xG |

## Payments — `/payments`
| Method | Path | Notes |
|--------|------|-------|
| GET | `/payments/subscription` | 🔑 current plan |
| POST | `/payments/subscribe` | 🔑 start premium |
| PATCH | `/payments/subscription/cancel` | 🔑 cancel |
| POST | `/payments/mpesa/initiate` | 🔑 M-Pesa STK push (stub) |

## Admin — `/admin` (all 🛡️)
| Method | Path | Notes |
|--------|------|-------|
| PATCH | `/admin/matches/{match_id}/score` | set score + auto-settle predictions |
| POST | `/admin/matches/sync` | sync fixtures from football-data |
| GET | `/admin/stats` | platform metrics |
| GET | `/admin/users` | list users |
| PATCH | `/admin/users/{user_id}/activate` · `/deactivate` | toggle user |
| GET | `/admin/venues/pending` | venue submissions queue |
| POST | `/admin/venues/{submission_id}/approve` · `/reject` | moderate venues |
