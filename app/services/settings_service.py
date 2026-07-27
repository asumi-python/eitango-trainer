import psycopg2.extras
from app.db import get_db

_DEFAULTS = {"mastery_mode": "manual", "streak_target": 3}


def get_settings() -> dict:
    with get_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM settings WHERE id = 1")
            row = cur.fetchone()
            return dict(row) if row else dict(_DEFAULTS)


def save_settings(mastery_mode: str, streak_target: int) -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO settings (id, mastery_mode, streak_target)
                VALUES (1, %s, %s)
                ON CONFLICT (id) DO UPDATE
                  SET mastery_mode  = EXCLUDED.mastery_mode,
                      streak_target = EXCLUDED.streak_target
                """,
                (mastery_mode, streak_target),
            )
