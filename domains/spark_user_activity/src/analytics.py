from pyspark.sql import DataFrame
from pyspark.sql.functions import (avg, col, count, countDistinct, round,
                                   row_number)
from pyspark.sql.window import Window


# get user latest login record
def latest_login(df: DataFrame) -> DataFrame:
    window = Window.partitionBy("user_id").orderBy(col("timestamp").desc())

    login_df = df.filter(col("event") == "login")
    return (
        login_df.withColumn("rn", row_number().over(window))
        .filter(col("rn") == 1)
        .drop("rn")
    )


def country_metrics(df: DataFrame) -> DataFrame:
    return df.groupBy("country").agg(
        count("*").alias("event_count"),
        countDistinct("user_id").alias("user_count"),
        round(avg("age"), 2).alias("avg_age"),
    )
