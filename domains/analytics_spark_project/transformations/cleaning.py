from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def clean_events(df: DataFrame) -> DataFrame:
    return df.dropna(subset=["user_id", "event_type", "event_time"]).filter(
        col("event_type").isin("view", "like", "comment", "share", "login", "logout")
    )
