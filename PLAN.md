# WorldCupDNA — Project Plan

## Overview
WorldCupDNA is a fan identity and prediction platform built 
for FIFA World Cup 2026 (June 11 – July 19, 2026). Fans build 
a football DNA profile, predict match scores, compete on a 
leaderboard, and find watch parties in Nairobi.

---

## Tech Stack
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS → Vercel
- **Backend:** FastAPI (Python) → Render
- **Database:** PostgreSQL (Neontech)
- **Auth:** JWT + Google OAuth
- **Payments:** Stripe + Mpesa
- **Notifications:** Email (SendGrid) + Push
- **Live Data:** football-data.org API

---

## Repository Structure
| Repo | Contents | URL |
|---|---|---|
| `worldcupdna-frontend` | Next.js app | github.com/abednegoingplaces/worldcupdna-frontend |
| `worldcupdna-backend` | FastAPI + Python | github.com/abednegoingplaces/worldcupdna-backend |

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
| GET  | /api/v1/auth/google | Google OAuth |

### Users
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/users/me | Get my profile |
| PATCH | /api/v1/users/me | Update my profile |
| DELETE | /api/v1/users/me | Delete my account |
| POST | /api/v1/users/me/avatar | Upload avatar |
| GET | /api/v1/users/{username} | Get user by username |

### Matches
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/matches | Get all matches |
| GET | /api/v1/matches/{id} | Get single match |
| GET | /api/v1/matches/live | Get live matches |

### Predictions
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/predictions | Get my predictions |
| POST | /api/v1/predictions | Create prediction |
| PATCH | /api/v1/predictions/{id} | Update prediction |
| DELETE | /api/v1/predictions/{id} | Delete prediction |
| POST | /api/v1/predictions/score/{match_id} | Score predictions |

### Leaderboard
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/leaderboard/global | Global rankings |
| GET | /api/v1/leaderboard/friends | Friends rankings |

### Venues
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/venues | Get all venues |
| POST | /api/v1/venues | Add venue |
| PATCH | /api/v1/venues/{id} | Update venue |
| DELETE | /api/v1/venues/{id} | Delete venue |

### Notifications
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/notifications | Get my notifications |
| POST | /api/v1/notifications | Send notification |
| PATCH | /api/v1/notifications/{id}/read | Mark as read |

### Payments
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/payments/subscribe | Create subscription |
| GET | /api/v1/payments/subscription | Get subscription status |
| POST | /api/v1/payments/webhook | Payment webhook |

### Admin
| Method | Endpoint | Description |
|---|---|---|
| PATCH | /api/v1/admin/matches/{id}/score | Update match score |
| POST | /api/v1/admin/matches/sync | Sync live match data |
| GET | /api/v1/admin/stats | Platform statistics |

---

## Database Tables
| Table | Purpose |
|---|---|
| `profiles` | Fan DNA profiles |
| `matches` | All 64 World Cup fixtures |
| `predictions` | User score predictions |
| `venues` | Nairobi watch party locations |
| `notifications` | User notifications |
| `subscriptions` | Payment subscriptions |

---

## Frontend Pages
| Page | Route | Status |
|---|---|---|
| Homepage | / | 🔨 In Progress |
| Fan Profile Builder | /profile/build | ⏳ Not Started |
| Profile Display | /profile | ⏳ Not Started |
| Match Hub | /matches | ⏳ Not Started |
| Leaderboard | /leaderboard | ⏳ Not Started |
| Watch Party Finder | /venues | ⏳ Not Started |
| Sign In / Sign Up | /auth | ⏳ Not Started |

---

## Build Phases

### Phase 1 — Foundation ✅
- [x] Next.js project setup
- [x] Database schema and migrations
- [x] Match and venue data seeded
- [x] Basic API routes built
- [x] Deployed to Render + Neontech

### Phase 2 — Backend Rebuild (In Progress)
- [ ] Modular folder structure
- [ ] Schemas layer (Pydantic)
- [ ] Services layer (business logic)
- [ ] Core layer (config, security, dependencies)
- [ ] Auth endpoints (JWT + Google OAuth)
- [ ] Full CRUD on all resources
- [ ] /api/v1/ versioning
- [ ] Payments (Stripe + Mpesa)
- [ ] Notifications
- [ ] Live match data (football-data.org)
- [ ] Admin endpoints

### Phase 3 — Frontend
- [ ] Homepage (Stitch design → Next.js)
- [ ] All 6 pages built
- [ ] Connected to FastAPI backend
- [ ] Deployed to Vercel

### Phase 4 — Launch
- [ ] Full testing
- [ ] SEO + Open Graph
- [ ] Social sharing (DNA badge cards)
- [ ] Deploy everything live
- [ ] June 11 — Tournament kickoff 🏆

---

## Live URLs
| Service | URL |
|---|---|
| Backend API | https://worldcupdna-backend.onrender.com |
| API Docs | https://worldcupdna-backend.onrender.com/docs |
| Database | Neontech PostgreSQL |
| Frontend | Coming soon — Vercel |

---

## Timeline
| Date | Milestone |
|---|---|
| May 28, 2026 | Project started |
| May 31, 2026 | Basic backend deployed |
| June 2, 2026 | Modular backend complete |
| June 5, 2026 | Frontend complete |
| June 10, 2026 | Full deployment |
| June 11, 2026 | 🏆 FIFA World Cup 2026 kicks off |

---

## Contributors
- Built by abednegoingplaces (Abeddy Ndimu)