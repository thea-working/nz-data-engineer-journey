import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import row_number

from domains.analytics_spark_project.utils.spark_session import create_spark


def compute_user_metrics(session_df: DataFrame) -> DataFrame:
    """
    compute user level metrics
    :param session_df : session metrics dataframe
    :return: user level aggregated metrics dataframe
    """
    return session_df.groupby("user_id").agg(
        F.count("*").alias("session_count"),
        F.avg("session_duration").alias("avg_session_duration"),
        F.sum("event_count").alias("event_count"),
    )


def compute_dau(event_df: DataFrame) -> DataFrame:
    """
    compute dau metrics
    :param event_df: enriched events dataframe
    :return: aggregated dataframe with event_date and dau
    """
    return (
        event_df.withColumn("event_date", F.to_date("event_time"))
        .select("event_date", "user_id")
        .distinct()
        .groupby("event_date")
        .agg(F.count("user_id").alias("dau"))
    )


# expand practicing
def compute_continuous_login(df: DataFrame) -> DataFrame:
    """
    compute users max continuous login days
    :param df: user_events dataframe containing user_id and event_date
    :return: new dataframe with user_id and max continuous login days
    """
    window_event = Window.partitionBy("user_id").orderBy("event_date")
    df = df.withColumn("rn", row_number().over(window_event))
    df = df.withColumn("group_key", F.expr("date_sub(event_date,rn)"))
    return (
        df.groupBy("user_id", "group_key")
        .agg(F.count("*").alias("date_count"))
        .groupBy("user_id")
        .agg(F.max("date_count").alias("max_count"))
    )


def compute_retention(df: DataFrame) -> DataFrame:
    window_event = Window.partitionBy("user_id").orderBy("event_date")
    df = df.withColumn("next_login_day", F.lead("event_date").over(window_event))
    df = df.withColumn(
        "is_retention",
        F.when(F.datediff("next_login_day", "event_date") == 1, 1).otherwise(0),
    )
    # retention rate
    retention = df.agg(
        (F.sum("is_retention") / F.countDistinct("user_id")).alias("day1_retention")
    )
    return retention


def compute_login_duration(df: DataFrame) -> DataFrame:
    # original user_id, login_date
    # target user_id, start_date, end_date, streak_days
    window_spec = Window.partitionBy("user_id").orderBy("login_date")
    extend_df = df.withColumn("rn", row_number().over(window_spec)).withColumn(
        "group_key", F.expr("date_sub(login_date,rn)")
    )
    streak_df = (
        extend_df.groupBy("user_id", "group_key")
        .agg(
            F.min("login_date").alias("start_date"),
            F.max("login_date").alias("end_date"),
            F.count("*").alias("streak_days"),
        )
        .filter(F.col("streak_days") > 1)
        .select("user_id", "start_date", "end_date", "streak_days")
    )

    # for cohort users compute retention based on month
    window_event = Window.partitionBy("user_id")
    retention_base = (
        (
            df.withColumn("first_login", F.min("login_date").over(window_event))
            .withColumn(
                "cohort_month", F.to_date(F.date_trunc("month", F.col("first_login")))
            )
            .withColumn(
                "login_month", F.to_date(F.date_trunc("month", F.col("login_date")))
            )
            .withColumn(
                "month_index",
                F.floor(F.months_between(F.col("login_month"), F.col("cohort_month"))),
            )
        )
        .groupBy("cohort_month", "month_index")
        .agg(F.countDistinct("user_id").alias("user_cnt"))
    )

    cohort_size = retention_base.filter(F.col("month_index") == 0).select(
        "cohort_month", F.col("user_cnt").alias("cohort_size")
    )
    retention_rate = retention_base.join(cohort_size, on="cohort_month").withColumn(
        "retention", F.col("user_cnt") / F.col("cohort_size")
    )
    final_df = (
        retention_rate.withColumn(
            "month_num", F.concat(F.lit("month_"), F.col("month_index").cast("string"))
        )
        .drop("month_index")
        .groupBy("cohort_month")
        .pivot("month_num")
        .agg(F.first("retention"))
    )
    final_df.explain()

    spark = create_spark()
    # data skew processing skew_keys = ["view"]
    # salting skewed keys
    salted_df = (
        extend_df.filter(F.col("event_type") == "view")
        .withColumn("salt", (F.rand() * 10).cast("int"))
        .withColumn(
            "salted_key", F.concat(F.col("event_type"), F.lit("_"), F.col("salt"))
        )
    )

    # expand dimension table (only contain skewed key)
    salt_df = spark.range(10).withColumnRenamed("id", "salt")
    dim_expand = streak_df.crossJoin(salt_df).withColumn(
        "salted_key", F.concat(F.col("event_type"), F.lit("_"), F.col("salt"))
    )

    salted_df.join(dim_expand, on="salted_key")

    return df
