from pyspark.sql import SparkSession, Window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import col, when, lit, row_number, to_timestamp, sum as spark_sum


def main():
    spark = (
        SparkSession.builder
        .appName("update_records")
        .master("local[*]")
        .getOrCreate()
    )

    current_users = [
        (101, "Alice", "Beijing", "2026-09-01 10:00:00"),
        (102, "Bob", "Shanghai", "2026-09-01 11:00:00"),
        (103, "Charlie", "Shenzhen", "2026-09-01 12:00:00"),
    ]
    incoming_users = [
        (101, "Alice", "Beijing", "2026-09-17 09:00:00"),
        (102, "Bob", "Hangzhou", "2026-09-17 09:10:00"),
        (104, "David", "Beijing", "2026-09-17 09:20:00"),
    ]
    users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("updated_at", StringType(), True)
    ])
    current_users_df = spark.createDataFrame(current_users, users_schema)
    incoming_users_df = spark.createDataFrame(incoming_users, users_schema)

    updated_users_df = (
        incoming_users_df.alias("i")
        .join(current_users_df.alias("c"),
              on="user_id",
              how="left"
              )
        .withColumn(
            "change_type",
            when(
                col("c.user_id").isNull(), lit("INSERT")
            )
            .when(
                (col("i.name") != col("c.name")) | (col("i.city") != col("c.city")), lit("UPDATE")
            )
            .otherwise(lit("NO_CHANGE"))
        )
        .select(
            "i.user_id",
            "i.name",
            "i.city",
            "i.updated_at",
            "change_type"
        )
    )

    updated_users_df.show()

    current_users = [
        (101, "Alice", "Beijing", "2026-09-01 10:00:00"),
        (102, "Bob", "Shanghai", "2026-09-01 11:00:00"),
        (103, "Charlie", "Shenzhen", "2026-09-01 12:00:00"),
    ]
    incoming_users = [
        (101, "Alice", "Beijing", "2026-09-17 08:00:00"),
        (101, "Alice", "Shanghai", "2026-09-17 09:00:00"),
        (102, "Bob", "Hangzhou", "2026-09-17 09:10:00"),
        (102, "Bob", "Shanghai", "2026-09-17 09:20:00"),
        (104, "David", "Beijing", "2026-09-17 10:00:00"),
    ]

    users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("updated_at", StringType(), True)
    ])
    current_users_df = spark.createDataFrame(current_users, users_schema)
    incoming_users_df = spark.createDataFrame(incoming_users, users_schema)
    current_users_df = current_users_df.withColumn(
        "updated_at",
        to_timestamp("updated_at")
    )

    incoming_users_df = incoming_users_df.withColumn(
        "updated_at",
        to_timestamp("updated_at")
    )

    user_window = Window.partitionBy("user_id").orderBy(col("updated_at").desc())
    deduplicated_incoming_users = (
        incoming_users_df.withColumn(
            "row_num",
            row_number().over(user_window)
        )
        .filter(col("row_num") == 1)
        .select("user_id", "name", "city", "updated_at")
    )

    updated_users_df = (
        deduplicated_incoming_users.alias("i")
        .join(current_users_df.alias("c"),
              on="user_id",
              how="left"
              )
        .withColumn(
            "change_type",
            when(
                col("c.user_id").isNull(), lit("INSERT")
            )
            .when(
                (col("i.name") != col("c.name")) | (col("i.city") != col("c.city")), lit("UPDATE")
            )
            .otherwise(lit("NO_CHANGE"))
        )
        .select(
            "i.user_id",
            "i.name",
            "i.city",
            "i.updated_at",
            "change_type"
        )
    )

    updated_users_df.show()

    change_type_count = updated_users_df.groupBy("change_type").count()
    change_type_count.show()

    statistic_count = updated_users_df.agg(
        spark_sum(when(col("change_type") == "INSERT", 1).otherwise(0)).alias("insert_count"),
        spark_sum(when(col("change_type") == "UPDATE", 1).otherwise(0)).alias("update_count")
    ).withColumn(
        "needs_upsert",
        col("insert_count") + col("update_count")
    )
    statistic_count.show()


if __name__ == "__main__":
    main()
