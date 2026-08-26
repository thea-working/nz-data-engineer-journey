import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def compute_user_metrics(session_df: DataFrame) -> DataFrame:
    return session_df.groupBy("user_id").agg(
        F.count("*").alias("session_count"),
        F.round(F.avg("session_duration_seconds"), 2).alias(
            "avg_session_duration_seconds"
        ),
        F.sum("event_count").alias("event_count"),
    )


def compute_daily_active_users(events_df: DataFrame) -> DataFrame:
    return (
        events_df.select("event_date", "user_id")
        .distinct()
        .groupBy("event_date")
        .agg(F.count("user_id").alias("daily_active_users"))
    )
