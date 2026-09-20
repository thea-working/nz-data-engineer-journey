from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import to_timestamp, col, row_number
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def main():
    spark = (
        SparkSession.builder
        .appName("update_records")
        .master("local[*]")
        .getOrCreate()
    )
    users = [
        (101, "Alice", "Beijing", "2026-09-01 10:00:00"),
        (102, "Bob", "Shanghai", "2026-09-01 11:00:00"),
        (103, "Charlie", "Shenzhen", "2026-09-01 12:00:00"),
    ]
    users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("updated_at", StringType(), True)
    ])
    users_df = spark.createDataFrame(users, users_schema)
    users_df = users_df.withColumn(
        "updated_at",
        to_timestamp("updated_at")
    )
    new_users = [
        (102, "Bob", "Hangzhou", "2026-09-17 09:00:00"),
        (103, "Charlie", "Shenzhen", "2026-09-17 09:30:00"),
        (104, "David", "Beijing", "2026-09-17 10:00:00"),
    ]
    new_users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("updated_at", StringType(), True)
    ])
    new_users_df = spark.createDataFrame(new_users, new_users_schema)
    new_users_df = new_users_df.withColumn(
        "updated_at",
        to_timestamp("updated_at")
    )

    add_users_df = new_users_df.alias("n").join(
        users_df.alias("o"),
        on="user_id",
        how="left_anti"
    )

    add_users_df.show()

    updated_users_df = new_users_df.alias("n").join(
        users_df.alias("o"),
        on="user_id",
        how="inner"
    ).filter(
        (col("n.updated_at") > col("o.updated_at")) &
        (
                (col("n.city") != col("o.city")) |
                (col("n.city") != col("o.city"))
        )
    ).select("n.*")

    updated_users_df.show()

    updates = [
        (101, "Alice", "Beijing", "2026-09-17 08:00:00"),
        (101, "Alice", "Shanghai", "2026-09-17 09:00:00"),
        (102, "Bob", "Hangzhou", "2026-09-17 09:10:00"),
        (102, "Bob", "Hangzhou", "2026-09-17 09:20:00"),
        (103, "Charlie", "Shenzhen", "2026-09-17 09:30:00"),
    ]
    updated_users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("updated_at", StringType(), True)
    ])
    updated_users_df = spark.createDataFrame(updates, updated_users_schema)

    updated_users_df = (
        updated_users_df.withColumn(
            "updated_at",
            to_timestamp("updated_at")
        )
    )

    user_window = Window.partitionBy("user_id").orderBy(col("updated_at").desc())
    updated_users_df = (
        updated_users_df
        .withColumn(
            "row_num",
            row_number().over(user_window)
        ).filter(col("row_num") == 1)
        .select(
            "user_id",
            "name",
            "city",
            "updated_at"
        )
    )
    updated_users_df.show()

    current_users = [
        (101, "Alice", "Beijing", "2026-09-01 10:00:00"),
        (102, "Bob", "Shanghai", "2026-09-01 11:00:00"),
        (103, "Charlie", "Shenzhen", "2026-09-01 12:00:00"),
    ]
    current_users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("updated_at", StringType(), True)
    ])
    current_users_df = spark.createDataFrame(current_users, current_users_schema)

    current_users_df = current_users_df.withColumn(
        "updated_at",
        to_timestamp("updated_at")
    )

    incoming_users = [
        (102, "Bob", "Hangzhou", "2026-09-17 09:00:00"),
        (102, "Bob", "Hangzhou", "2026-09-17 09:30:00"),
        (103, "Charlie", "Shenzhen", "2026-09-17 09:10:00"),
        (104, "David", "Beijing", "2026-09-17 10:00:00"),
    ]
    incoming_users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("updated_at", StringType(), True)
    ])
    incoming_users_df = spark.createDataFrame(incoming_users, incoming_users_schema)

    incoming_users_df = incoming_users_df.withColumn(
        "updated_at",
        to_timestamp("updated_at")
    )

    user_window = Window.partitionBy("user_id").orderBy(col("updated_at").desc())
    incoming_users_df = (
        incoming_users_df.withColumn(
            "row_num",
            row_number().over(user_window)
        )
        .filter(col("row_num") == 1)
        .select(
            "user_id",
            "name",
            "city",
            "updated_at"
        )
    )

    all_users_df = (
        incoming_users_df.unionByName(current_users_df)
        .withColumn(
            "row_num",
            row_number().over(user_window)
        )
        .filter(col("row_num") == 1)
        .select(
            "user_id",
            "name",
            "city",
            "updated_at"
        )
    )

    all_users_df.show()


if __name__ == "__main__":
    main()
