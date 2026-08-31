from pyspark.sql import SparkSession, Window
from pyspark.sql.types import *
from pyspark.sql.functions import *


def main():
    spark = (
        SparkSession.builder
        .appName("dataframe basic")
        .master("local")
        .getOrCreate()
    )
    orders = [
        (1, 101, 100.0, "2026-08-28 10:00:00"),
        (2, 101, 150.0, "2026-08-28 11:00:00"),
        (3, 101, 200.0, "2026-08-28 12:00:00"),
        (4, 102, 80.0, "2026-08-28 09:00:00"),
        (5, 102, 120.0, "2026-08-28 10:30:00"),
        (6, 103, 200.0, "2026-08-28 14:00:00"),
    ]
    schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("event_time", StringType(), True),
    ])

    orders_df = spark.createDataFrame(orders, schema)

    user_orders_df = (
        orders_df.withColumn(
            "previous_amount",
            lag("amount").over(
                Window.partitionBy("user_id")
                .orderBy("event_time")
            )
        ).withColumn(
            "amount_diff",
            col("amount") - col("previous_amount")
        ).select(
            "user_id",
            "order_id",
            "amount",
            "previous_amount",
            "amount_diff"
        )
    )

    user_orders_df.show()

    orders = [
        (1, 101, 100.0, "2026-08-28 10:00:00"),
        (2, 101, 150.0, "2026-08-28 11:00:00"),
        (3, 101, 200.0, "2026-08-28 12:00:00"),
        (4, 102, 80.0, "2026-08-28 09:00:00"),
        (5, 102, 120.0, "2026-08-28 10:30:00"),
    ]
    schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("event_time", StringType(), True),
    ])

    orders_df = spark.createDataFrame(orders, schema)
    user_total_orders_df = (
        orders_df.withColumn(
            "running_total",
            sum("amount").over(
                Window.partitionBy("user_id")
                .orderBy("event_time")
                .rowsBetween(
                    Window.unboundedPreceding,
                    Window.currentRow
                )
            )
        ).select(
            "user_id",
            "order_id",
            "amount",
            "running_total"
        )
    )
    user_total_orders_df.show()

    orders = [
        (1, 101, 100.0, "2026-08-28 10:00:00"),
        (2, 101, 150.0, "2026-08-28 11:00:00"),
        (3, 101, 120.0, "2026-08-28 12:00:00"),
        (4, 102, 200.0, "2026-08-28 09:00:00"),
        (5, 102, 300.0, "2026-08-28 10:00:00"),
    ]
    schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("event_time", StringType(), True),
    ])

    orders_df = spark.createDataFrame(orders, schema)
    user_orders_df = (
        orders_df.withColumn(
            "previous_amount",
            lag("amount").over(
                Window.partitionBy("user_id")
                .orderBy("event_time")
            )
        ).withColumn(
            "amount_change_pct",
            when(
                col("previous_amount").isNull() |
                (col("previous_amount") == 0),
                None
            ).otherwise(
                round((col("amount") - col("previous_amount")) / col("previous_amount") * 100, 2))
        ).select(
            "user_id",
            "order_id",
            "amount",
            "previous_amount",
            "amount_change_pct"
        )
    )

    user_orders_df.show()


if __name__ == "__main__":
    main()
