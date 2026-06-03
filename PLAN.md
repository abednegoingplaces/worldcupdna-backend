# WorldCupDNA — Project Plan

## Overview
WorldCupDNA is a fan identity and prediction platform built for FIFA World Cup 2026 (June 11 – July 19, 2026). Fans build a football DNA profile, predict match scores, compete on a leaderboard, and find watch parties anywhere in the world.

---

## Tech Stack
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS → Vercel
- **Backend:** FastAPI (Python) → Render
- **Database:** PostgreSQL (Neontech)
- **Auth:** JWT + Google OAuth
- **Payments:** Stripe + Mpesa
- **Notifications:** In-app + Email
- **Live Data:** football-data.org API

---

## Repositories
| Repo | Contents | URL |
|---|---|---|
| `worldcupdna-backend` | FastAPI + Python | github.com/abednegoingplaces/worldcupdna-backend |
| `worldcupdna-frontend` | Next.js + TypeScript | github.com/abednegoingplaces/worldcupdna-frontend |

---

## Backend Structure (Modular)
---

## API Endpoints (/api/v1/)

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/auth/register | Register new user |
| POST | /api/v1/auth/login | Login, returns JWT |
| POST | /api/v1/auth/logout | Logout |
| POST | /api/v1/auth/refresh | Refresh JWT token |
| POST | /api/v1/auth/verify-email | Verify email |
| POST | /api/v1/auth/password-reset/request | Request password reset |
| POST | /api/v1/auth/password-reset/confirm | Confirm password reset |
| GET | /api/v1/auth/google | Google OAuth |
| GET | /api/v1/auth/google/callback | Google OAuth callback |

### Users
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/users/me | Get my profile |
| PATCH | /api/v1/users/me | Update my profile |
| DELETE | /api/v1/users/me | Delete my account |
| POST | /api/v1/users/me/avatar | Upload avatar |
| PUT | /api/v1/users/me/interests | Update interests |
| GET | /api/v1/users/search | Search users |
| GET | /api/v1/users/{username} | Get user by username |

### Matches
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/matches/ | Get all matches (DB) |
| GET | /api/v1/matches/live | Live scores (football-data.org) |
| GET | /api/v1/matches/upcoming | Upcoming matches (football-data.org) |
| GET | /api/v1/matches/standings | Group standings (football-data.org) |
| GET | /api/v1/matches/{id} | Get single match |

### Predictions
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/predictions/ | Get my predictions |
| POST | /api/v1/predictions/ | Create prediction |
| PATCH | /api/v1/predictions/{id} | Update prediction |
| DELETE | /api/v1/predictions/{id} | Delete prediction |
| POST | /api/v1/predictions/score/{match_id} | Score predictions |

### Leaderboard
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/leaderboard/ | Global rankings |

### Venues
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/venues/ | Get venues (filter by city/country/location) |
| GET | /api/v1/venues/{id} | Get single venue |
| POST | /api/v1/venues/submit | Submit a venue (anyone, anywhere) |
| GET | /api/v1/venues/submissions/pending | Admin — pending submissions |
| PATCH | /api/v1/venues/submissions/{id}/approve | Admin — approve submission |
| PATCH | /api/v1/venues/submissions/{id}/reject | Admin — reject submission |

### Notifications
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/notifications/ | Get my notifications |
| POST | /api/v1/notifications/ | Send notification |
| PATCH | /api/v1/notifications/{id}/read | Mark as read |
| PATCH | /api/v1/notifications/read-all | Mark all as read |
| DELETE | /api/v1/notifications/{id} | Delete notification |

### Payments
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/payments/subscribe | Create subscription |
| GET | /api/v1/payments/subscription | Get subscription status |
| PATCH | /api/v1/payments/subscription/cancel | Cancel subscription |
| POST | /api/v1/payments/mpesa/initiate | Initiate Mpesa STK push |
| POST | /api/v1/payments/webhook | Payment webhook |

### Admin
| Method | Endpoint | Description |
|---|---|---|
| PATCH | /api/v1/admin/matches/{id}/score | Update match score + auto-score predictions |
| GET | /api/v1/admin/stats | Platform statistics |
| GET | /api/v1/admin/users | Get all users |
| PATCH | /api/v1/admin/users/{id}/deactivate | Deactivate user |
| POST | /api/v1/admin/matches/sync | Sync matches from football-data.org |

---

## Database Tables
| Table | Purpose |
|---|---|
| `users` | Fan accounts + DNA profiles |
| `matches` | All World Cup fixtures |
| `predictions` | User score predictions |
| `venues` | Watch party locations (global) |
| `venue_submissions` | User-submitted venues pending approval |
| `notifications` | User notifications |
| `subscriptions` | Payment subscriptions |

---

## Live URLs
| Service | URL |
|---|---|
| Backend API | https://worldcupdna-backend.onrender.com |
| API Docs | https://worldcupdna-backend.onrender.com/docs |
| Database | Neontech PostgreSQL |
| Frontend | Coming soon — Vercel |

---

## Build Status

### Backend ✅ COMPLETE
- [x] Modular folder structure
- [x] All 9 routers built
- [x] /api/v1/ versioning
- [x] JWT Auth + Google OAuth
- [x] Full CRUD on predictions, users, venues
- [x] Notifications system
- [x] Payments (Stripe placeholder + Mpesa placeholder)
- [x] Admin endpoints with auto-scoring
- [x] Live match data from football-data.org
- [x] Global venue support + submission system
- [x] Deployed on Render

### Frontend ⏳ IN PROGRESS
- [x] Next.js project setup
- [x] Supabase removed, FastAPI client added
- [x] Deployed to Vercel
- [ ] Homepage
- [ ] Auth page
- [ ] Fan Profile Builder
- [ ] Match Hub
- [ ] Leaderboard
- [ ] Watch Party Finder

---

## Frontend Pages
| Page | Route | Status |
|---|---|---|
| Homepage | / | ⏳ Not Started |
| Sign In / Sign Up | /auth | ⏳ Not Started |
| Fan Profile Builder | /profile/build | ⏳ Not Started |
| My Profile | /profile | ⏳ Not Started |
| Match Hub | /matches | ⏳ Not Started |
| Leaderboard | /leaderboard | ⏳ Not Started |
| Watch Party Finder | /venues | ⏳ Not Started |

---

## Timeline
| Date | Milestone |
|---|---|
| May 28, 2026 | Project started |
| May 31, 2026 | Basic backend deployed |
| June 2, 2026 | Modular backend complete |
| June 3, 2026 | All routers + live data done ✅ |
| June 5, 2026 | Frontend complete |
| June 8, 2026 | Everything connected |
| June 10, 2026 | Polish + testing |
| June 11, 2026 | 🏆 FIFA World Cup 2026 kicks off |

---

## Contributors
- Built by Abeddy Ndimu