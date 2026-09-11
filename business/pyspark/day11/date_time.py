from pyspark.sql import SparkSession, Window
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import (col, to_timestamp, to_date, month, date_diff, lit,
                                   min as func_min, max as func_max, lag, count, timestamp_diff,
                                   sum as func_sum)


def main():
    spark = (
        SparkSession.builder
        .appName("PySpark date time processing")
        .master("local[*]")
        .getOrCreate()
    )

    events = [
        (1, 101, "login", "2026-09-01 09:15:00"),
        (2, 101, "purchase", "2026-09-01 10:20:00"),
        (3, 102, "login", "2026-09-02 08:30:00"),
        (4, 102, "logout", "2026-09-02 18:00:00"),
        (5, 103, "login", "2026-09-05 12:00:00"),
        (6, 101, "login", "2026-09-10 09:00:00"),
        (7, 104, "login", None),
    ]
    events_schema = StructType([
        StructField("event_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("event_type", StringType(), True),
        StructField("event_time", StringType(), True)
    ])

    events_df = spark.createDataFrame(events, events_schema)
    cleaned_events = (
        events_df
        .withColumn(
            "event_time",
            to_timestamp(col("event_time"))
        )
        .withColumn(
            "event_date",
            to_date(col("event_time"))
        )
        .withColumn(
            "event_month",
            month(col("event_time"))
        )
        .filter(
            (col("event_time").isNotNull()) &
            (col("event_date") >= '2026-09-01') &
            (col("event_date") <= '2026-09-05')
        )
        .withColumn(
            "days_diff",
            date_diff(lit('2026-09-10'), col("event_date"))
        )
    )
    cleaned_events.show()

    user_window = Window.partitionBy("user_id")
    event_window = Window.partitionBy("user_id").orderBy("event_time")
    agg_events_df = (
        events_df
        .withColumn(
            "first_event_time",
            func_min(col("event_time")).over(user_window)
        )
        .withColumn(
            "last_event_time",
            func_max(col("event_time")).over(user_window)
        )
        .withColumn(
            "previous_event_time",
            lag(col("event_time")).over(event_window)
        )
        .withColumn(
            "gap_minutes",
            timestamp_diff("MINUTE", col("previous_event_time"), col("event_time"))
        )
        .drop("event_id")
    )

    active_days_df = (
        events_df
        .filter(col("event_time").isNotNull())
        .select(
            "user_id",
            to_date(col("event_time")).alias("event_date")
        )
        .distinct()
        .groupBy("user_id")
        .agg(
            count("*").alias("active_days")
        )
    )

    agg_events_df = agg_events_df.join(
        active_days_df,
        on="user_id",
        how="left"
    )

    agg_events_df.show()

    events = [
        (1, 101, "login", "2026-09-01 09:15:00"),
        (2, 101, "purchase", "2026-09-01 10:20:00"),
        (3, 101, "login", "2026-09-01 18:30:00"),
        (4, 102, "login", "2026-09-02 08:30:00"),
        (5, 102, "logout", "2026-09-02 18:00:00"),
        (6, 103, "login", "2026-09-05 12:00:00"),
        (7, 104, "login", None),
        (8, 105, "purchase", "2026-09-06 14:00:00"),
        (9, 105, "purchase", "2026-09-06 14:05:00"),
        (10, 105, "logout", "2026-09-06 20:00:00"),
        (11, 106, "login", "2026-09-07 09:00:00"),
        (11, 106, "login", "2026-09-07 09:00:00"),
    ]
    events_schema = StructType([
        StructField("event_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("event_type", StringType(), True),
        StructField("event_time", StringType(), True)
    ])
    events_df = spark.createDataFrame(events, events_schema)

    event_record_window = Window.partitionBy("event_id")
    cleaned_events = (
        events_df
        .withColumn(
            "event_time",
            to_timestamp(col("event_time"))
        )
        .filter(
            (col("user_id").isNotNull()) &
            (col("event_type").isNotNull()) &
            (col("event_time").isNotNull())
        )
        .withColumn(
            "event_num",
            count("*").over(event_record_window)
        )
        .filter(col("event_num") == 1)
        .withColumn(
            "event_date",
            to_date(col("event_time"))
        )
    )

    agg_events_df = (
        cleaned_events
        .withColumn(
            "first_event_time",
            func_min(col("event_time")).over(user_window)
        )
        .withColumn(
            "last_event_time",
            func_max(col("event_time")).over(user_window)
        )
        .withColumn(
            "previous_event_time",
            lag(col("event_time")).over(event_window)
        )
        .withColumn(
            "gap_minutes",
            timestamp_diff("MINUTE", col("previous_event_time"), col("event_time"))
        )
    )

    active_days_df = (
        cleaned_events
        .filter(col("event_time").isNotNull())
        .select(
            "user_id",
            to_date(col("event_time")).alias("event_date")
        )
        .distinct()
        .groupBy("user_id")
        .agg(
            count("*").alias("active_days")
        )
    )

    agg_events_df = agg_events_df.join(
        active_days_df,
        on="user_id",
        how="left"
    ).select(
        "event_id",
        "user_id",
        "event_type",
        "event_time",
        "event_date",
        "previous_event_time",
        "gap_minutes",
        "first_event_time",
        "last_event_time",
        "active_days"
    )

    agg_events_df.show()


if __name__ == "__main__":
    main()
