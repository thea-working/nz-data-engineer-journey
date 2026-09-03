from pyspark.sql import SparkSession, Window
from pyspark.sql.types import *
from pyspark.sql.functions import *


def main():
    spark = (
        SparkSession.builder
        .appName("deduplication")
        .master("local[*]")
        .getOrCreate()
    )
    users = [
        (101, "Alice", "Beijing"),
        (102, "Bob", "Shanghai"),
        (101, "Alice", "Beijing"),
        (103, "Charlie", "Guangzhou"),
        (102, "Bob", "Shanghai"),
    ]
    users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True)
    ])
    users_df = spark.createDataFrame(users, users_schema)
    users_deduplicated = (
        users_df.dropDuplicates()
        .orderBy("user_id")
    )
    users_deduplicated.show()

    users = [
        (101, "Alice", "Beijing", "2026-09-01 10:00:00"),
        (101, "Alice", "Shanghai", "2026-09-02 09:00:00"),
        (102, "Bob", "Shanghai", "2026-09-01 08:00:00"),
        (102, "Bob", "Beijing", "2026-09-03 12:00:00"),
        (103, "Charlie", "Guangzhou", "2026-09-01 15:00:00"),
    ]
    users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("event_time", StringType(), True),
    ])
    users_df = spark.createDataFrame(users, users_schema)
    users_deduplicated = (
        users_df.select(
            col("user_id"),
            col("name"),
            col("city"),
            col("event_time"),
            row_number().over(
                Window.partitionBy("user_id")
                .orderBy(col("event_time").desc())
            ).alias("row_num")
        ).filter(col("row_num") == 1)
        .drop("row_num")
    )
    users_deduplicated.show()

    user_events = [
        (101, "Alice", "Beijing", "active", "2026-09-01 10:00:00"),
        (101, "Alice", "Shanghai", "active", "2026-09-02 09:00:00"),
        (101, "Alice", "Shanghai", "inactive", "2026-09-03 14:00:00"),
        (102, "Bob", "Shanghai", "active", "2026-09-01 08:00:00"),
        (102, "Bob", "Beijing", "active", "2026-09-03 12:00:00"),
        (103, "Charlie", "Guangzhou", "active", "2026-09-01 15:00:00"),
    ]
    users_events_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("status", StringType(), True),
        StructField("event_time", StringType(), True),
    ])

    users_events_df = spark.createDataFrame(user_events, users_events_schema)
    status_agg_df = (
        users_events_df.withColumn(
            "row_num",
            row_number().over(
                Window.partitionBy("user_id")
                .orderBy(col("event_time").desc())
            )
        ).filter(col("row_num") == 1)
        .drop("row_num")
        .groupBy(col("status"))
        .agg(count("user_id").alias("count"))
    )
    status_agg_df.show()


if __name__ == "__main__":
    main()
