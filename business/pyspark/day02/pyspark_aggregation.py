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
        (1, 101, 100.0, "completed"),
        (2, 101, 50.0, "completed"),
        (3, 102, 200.0, "completed"),
        (4, 102, 80.0, "cancelled"),
        (5, 103, 120.0, "completed"),
        (6, 101, 70.0, "cancelled"),
        (7, 103, 200.0, "completed"),
    ]

    schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("status", StringType(), True)
    ])

    orders_df = spark.createDataFrame(orders, schema)

    agg_orders = (
        orders_df
        .filter(col("status") == "completed")
        .groupBy("user_id")
        .agg(
            count("order_id").alias("total_orders"),
            sum("amount").alias("total_amount"),
            avg("amount").alias("avg_amount"),
        )
        .orderBy(col("total_amount").desc())
    )

    agg_orders.show()

    customers = [
        (1, "Alice", 25, "Beijing"),
        (2, "Bob", None, "Shanghai"),
        (3, "Charlie", 30, None),
        (4, "David", None, None),
        (5, "Emma", 28, "Shanghai"),
    ]
    customers_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("city", StringType(), True)
    ])
    customers_df = spark.createDataFrame(customers, customers_schema)

    customers_df.filter(col("age").isNull()).show()

    norm_customers = customers_df.fillna({
        "age": 0,
        "city": "Unknown"
    }
    )

    norm_customers.show()

    orders = [
        (1, 101, 100.0, "2026-08-28 10:00:00"),
        (2, 102, 200.0, "2026-08-28 10:05:00"),
        (3, 101, 150.0, "2026-08-28 10:10:00"),
        (2, 102, 200.0, "2026-08-28 10:05:00"),
        (3, 101, 180.0, "2026-08-28 10:15:00"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("event_time", StringType(), True),
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    distinct_orders = ((
                           orders_df.withColumn(
                               "row_num",
                               row_number().over(
                                   Window.partitionBy("order_id")
                                   .orderBy(col("event_time").desc()))
                           )
                       )
                       .filter(col("row_num") == 1)
                       .select("order_id", "user_id", "amount", "event_time")
                       )
    distinct_orders.show()


if __name__ == "__main__":
    main()
