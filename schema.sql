-- words テーブル
CREATE TABLE public.words (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  english     TEXT NOT NULL,
  meaning     TEXT NOT NULL,
  is_mastered BOOLEAN NOT NULL DEFAULT FALSE,
  streak      INTEGER NOT NULL DEFAULT 0,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- settings テーブル（id=1 の行を upsert で使い回す設計）
CREATE TABLE public.settings (
  id            INTEGER PRIMARY KEY,
  mastery_mode  TEXT NOT NULL DEFAULT 'manual',
  streak_target INTEGER NOT NULL DEFAULT 3
);
