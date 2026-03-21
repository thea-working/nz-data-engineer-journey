from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_timestamp


# clean user logs , remove records with missing event
def clean_user_logs(df: DataFrame) -> DataFrame:
    return df.dropna(subset=["event"]).withColumn(
        "timestamp", to_timestamp(col("timestamp"), "YYYY-MM-DD HH:mm:ss")
    )


# clean user profile
# remove duplicate records; cast datatype
def clean_user_profile(df: DataFrame) -> DataFrame:
    return df.dropDuplicates(["user_id"]).withColumn("age", col("age").cast("int"))
