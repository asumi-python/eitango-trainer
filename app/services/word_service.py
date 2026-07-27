import psycopg2.extras
from app.db import get_db


def _fetchall(conn, sql, params=()):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]


def _fetchone(conn, sql, params=()):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None


def get_random_word() -> dict | None:
    with get_db() as conn:
        return _fetchone(
            conn,
            "SELECT * FROM words WHERE is_mastered = FALSE ORDER BY RANDOM() LIMIT 1",
        )


def get_all_active_words() -> list[dict]:
    with get_db() as conn:
        return _fetchall(
            conn,
            "SELECT * FROM words WHERE is_mastered = FALSE ORDER BY created_at DESC",
        )


def create_word(english: str, meaning: str) -> dict:
    with get_db() as conn:
        return _fetchone(
            conn,
            "INSERT INTO words (english, meaning) VALUES (%s, %s) RETURNING *",
            (english, meaning),
        )


def record_answer(word_id: str, correct: bool, settings: dict) -> bool:
    """Update streak and check mastery. Returns True if word was just mastered."""
    with get_db() as conn:
        row = _fetchone(conn, "SELECT streak FROM words WHERE id = %s", (word_id,))
        if not row:
            return False

        current_streak = row["streak"]
        new_streak = current_streak + 1 if correct else 0

        mastered = (
            correct
            and settings["mastery_mode"] == "auto"
            and new_streak >= settings["streak_target"]
        )

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE words SET streak = %s, is_mastered = %s WHERE id = %s",
                (new_streak, mastered, word_id),
            )

        return mastered


def mark_mastered(word_id: str) -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE words SET is_mastered = TRUE WHERE id = %s", (word_id,))


def soft_delete_word(word_id: str) -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE words SET is_mastered = TRUE WHERE id = %s", (word_id,))
