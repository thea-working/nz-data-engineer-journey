import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window

#  Define session boundary:
#  A new session starts if the time gap between consecutive events exceeds 30 minutes


def sessionize(df: DataFrame) -> DataFrame:
    """
    Assign session IDs to user events based on inactivity gap.

    A new session is created when the time difference between consecutive events
    for the same user exceeds 30 minutes.

    :param df: Input event DataFrame
    :return:  new DataFrame with session_id column
    """
    window_spec = Window.partitionBy("user_id").orderBy("event_time")

    # compute user's previous event time for each user event
    df = df.withColumn("prev_time", F.lag("event_time").over(window_spec))

    # compute time difference between current event time and previous event time
    df = df.withColumn(
        "time_diff", F.unix_timestamp("event_time") - F.unix_timestamp("prev_time")
    )

    # identify whether current event is a new session
    df = df.withColumn(
        "new_session",
        F.when(F.col("time_diff").isNull() | (F.col("time_diff") > 1800), 1).otherwise(
            0
        ),
    )

    # define session_id
    df = df.withColumn("session_id", F.sum(F.col("new_session")).over(window_spec))

    return df


def aggregate_session_metrics(df: DataFrame) -> DataFrame:
    """
    Compute session-level metrics.

    :param df: Sessionized event DataFrame
    :return: Aggregated session metrics DataFrame
    """
    user_sessions = df.groupBy("user_id", "session_id").agg(
        F.count("*").alias("event_count"),
        F.min("event_time").alias("start_time"),
        F.max("event_time").alias("end_time"),
    )

    user_sessions = user_sessions.withColumn(
        "session_duration",
        F.unix_timestamp("end_time") - F.unix_timestamp("start_time"),
    )

    return user_sessions
