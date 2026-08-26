from pyspark.sql import DataFrame
from pyspark.sql.functions import broadcast


def build_enriched_events(
    events_df: DataFrame, users_df: DataFrame, content_df: DataFrame
) -> DataFrame:
    return events_df.join(broadcast(users_df), on="user_id", how="left").join(
        broadcast(content_df), on="content_id", how="left"
    )
