import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras


@contextmanager
def get_db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
