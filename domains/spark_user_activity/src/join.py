from pyspark.sql import DataFrame


# join user_logs, user_profile, country_info
def build_enriched_logs(
    user_logs: DataFrame, user_profile: DataFrame, country_info: DataFrame
) -> DataFrame:
    return user_logs.join(user_profile, on="user_id", how="left").join(
        country_info, on="country", how="left"
    )
