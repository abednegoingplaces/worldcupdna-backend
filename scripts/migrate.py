"""Lightweight idempotent migration for the live (Neon) database.

The app uses ``create_all`` for fresh tables, but that does NOT add new columns
to tables that already exist. This script issues ``ALTER TABLE ... ADD COLUMN
IF NOT EXISTS`` for columns introduced during the v2 rebuild so an existing
deployment can be upgraded in place without data loss.

Run:  python -m scripts.migrate
"""
from sqlalchemy import text

from app.core.database import engine

STATEMENTS = [
    # users.total_points was missing in some deployments
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS total_points INTEGER NOT NULL DEFAULT 0",
    # DNA fields persisted at registration
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS favorite_team VARCHAR",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS tactical_style VARCHAR",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS rivalry_level VARCHAR",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token VARCHAR",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR",
    # predictions standardised on predicted_home / predicted_away
    "ALTER TABLE predictions ADD COLUMN IF NOT EXISTS predicted_home INTEGER",
    "ALTER TABLE predictions ADD COLUMN IF NOT EXISTS predicted_away INTEGER",
    "ALTER TABLE predictions ADD COLUMN IF NOT EXISTS points INTEGER DEFAULT 0",
    "ALTER TABLE predictions ADD COLUMN IF NOT EXISTS scored INTEGER DEFAULT 0",
    # matches enriched with crests / codes / stage metadata
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS external_id VARCHAR",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS home_team_code VARCHAR",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS away_team_code VARCHAR",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS home_team_crest VARCHAR",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS away_team_crest VARCHAR",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS stage_code VARCHAR",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS matchday INTEGER",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS venue VARCHAR",
    # timestamp columns were added to legacy tables after their first deploy
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now()",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now()",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ",
    "ALTER TABLE predictions ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now()",
    "ALTER TABLE predictions ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ",
]


def main() -> None:
    with engine.begin() as conn:
        for stmt in STATEMENTS:
            try:
                conn.execute(text(stmt))
                print(f"✓ {stmt}")
            except Exception as exc:  # pragma: no cover - best-effort per-statement
                print(f"⚠ skipped ({exc}): {stmt}")
    print("✅ Migration complete")


if __name__ == "__main__":
    main()
