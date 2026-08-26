from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def _read_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")


def build_daily_active_users_sql() -> str:
    return _read_sql("daily_active_users.sql")


def build_user_engagement_sql() -> str:
    return _read_sql("user_engagement.sql")


def build_content_ranking_sql(top_n: int) -> str:
    return _read_sql("content_ranking.sql").format(top_n=top_n)
