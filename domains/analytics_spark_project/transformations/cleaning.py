from pyspark.sql import DataFrame
from pyspark.sql import functions as F

ALLOWED_EVENT_TYPES = ("view", "like", "comment", "share", "login", "logout")
ALLOWED_DEVICES = ("android", "ios", "web")


def clean_events(df: DataFrame) -> DataFrame:
    return (
        df.select(
            "event_id",
            "user_id",
            "content_id",
            "event_type",
            "device",
            "country",
            "event_time",
        )
        .withColumn("event_time", F.to_timestamp("event_time"))
        .dropna(subset=["event_id", "user_id", "event_type", "event_time"])
        .dropDuplicates(["event_id"])
        .filter(F.col("event_type").isin(ALLOWED_EVENT_TYPES))
        .filter(F.col("device").isin(ALLOWED_DEVICES))
        .withColumn("country", F.coalesce(F.col("country"), F.lit("UNKNOWN")))
        .withColumn("event_date", F.to_date("event_time"))
    )


def clean_users(df: DataFrame) -> DataFrame:
    return (
        df.select("user_id", "age", "signup_country", "signup_date")
        .withColumn("age", F.col("age").cast("int"))
        .withColumn("signup_date", F.to_date("signup_date"))
        .dropna(subset=["user_id", "age", "signup_country", "signup_date"])
        .dropDuplicates(["user_id"])
        .filter((F.col("age") >= 13) & (F.col("age") <= 100))
    )


def clean_content(df: DataFrame) -> DataFrame:
    return (
        df.select("content_id", "category", "author_id", "publish_time")
        .withColumn("publish_time", F.to_timestamp("publish_time"))
        .dropna(subset=["content_id", "category", "author_id", "publish_time"])
        .dropDuplicates(["content_id"])
    )
