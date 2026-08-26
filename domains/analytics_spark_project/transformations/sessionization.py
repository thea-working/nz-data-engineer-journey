import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window

SESSION_GAP_SECONDS = 30 * 60


def sessionize(df: DataFrame) -> DataFrame:
    window_spec = Window.partitionBy("user_id").orderBy("event_time")

    with_prev = df.withColumn(
        "previous_event_time", F.lag("event_time").over(window_spec)
    )
    with_gap = with_prev.withColumn(
        "gap_seconds",
        F.unix_timestamp("event_time") - F.unix_timestamp("previous_event_time"),
    )
    with_markers = with_gap.withColumn(
        "new_session_flag",
        F.when(
            F.col("gap_seconds").isNull()
            | (F.col("gap_seconds") > SESSION_GAP_SECONDS),
            1,
        ).otherwise(0),
    )

    return with_markers.withColumn(
        "session_id",
        F.sum("new_session_flag").over(window_spec),
    )


def aggregate_session_metrics(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("user_id", "session_id")
        .agg(
            F.count("*").alias("event_count"),
            F.min("event_time").alias("session_start_time"),
            F.max("event_time").alias("session_end_time"),
        )
        .withColumn(
            "session_duration_seconds",
            F.unix_timestamp("session_end_time")
            - F.unix_timestamp("session_start_time"),
        )
        .withColumn("session_date", F.to_date("session_start_time"))
    )
