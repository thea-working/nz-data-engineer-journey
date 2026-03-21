from pyspark.sql import DataFrame
from pyspark.sql.functions import broadcast


def join_users(events_df: DataFrame, users_df: DataFrame) -> DataFrame:
    return events_df.join(
        broadcast(users_df),  # small dataset broadcast
        on="user_id",
        how="left",
    )


def join_content(events_df: DataFrame, content_df: DataFrame) -> DataFrame:
    return events_df.join(
        broadcast(content_df),
        on="content_id",
        how="left",
    )
