from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, col, to_date, count, sum as spark_sum, countDistinct
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType


def main():
    spark = (
        SparkSession.builder
        .appName("Incremental Processing")
        .master("local[*]")
        .getOrCreate()
    )

    orders = [
        (1, 101, 100.0, "completed", "2026-09-25 10:00:00"),
        (2, 102, 80.0, "completed", "2026-09-26 11:30:00"),
        (3, 103, 120.0, "cancelled", "2026-09-26 14:00:00"),
        (4, 104, 150.0, "completed", "2026-09-27 09:20:00"),
        (5, 105, 90.0, "completed", "2026-09-28 13:00:00"),
        (6, 106, 200.0, "completed", "2026-09-28 15:00:00"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("status", StringType(), True),
        StructField("order_time", StringType(), True)
    ])

    orders_df = spark.createDataFrame(orders, orders_schema)
    # 将 order_time 从 STRING 转换成 TimestampType。
    # 新增 order_date，类型为 DateType，只保留日期部分。
    # 只保留 2026-09-28 的订单。
    # 在这些订单中，只保留 status = "completed"
    cleaned_orders_df = (
        orders_df
        .withColumn(
            "order_time",
            to_timestamp(col("order_time"), "yyyy-MM-dd HH:mm:ss")
        )
        .withColumn(
            "order_date",
            to_date(col("order_time"))
        )
        .filter(
            (col("order_date") == "2026-09-28") &
            (col("status") == "completed")
        )
        .select(
            "order_id",
            "customer_id",
            "amount",
            "order_date"
        )
    )

    cleaned_orders_df.show()

    date_aggregated_orders = (
        orders_df
        .withColumn(
            "order_time",
            to_timestamp(col("order_time"), "yyyy-MM-dd HH:mm:ss")
        )
        .withColumn(
            "order_date",
            to_date(col("order_time"))
        )
        .filter(col("status") == "completed")
        .groupBy(col("order_date"))
        .agg(
            count(col("order_id")).alias("total_orders"),
            spark_sum(col("amount")).alias("total_sales"),
            countDistinct(col("customer_id")).alias("unique_customers")
        )
    )

    date_aggregated_orders.show()

    orders = [
        (1, 101, 100.0, "completed", "2026-09-27 10:00:00"),
        (2, 102, 80.0, "completed", "2026-09-27 11:00:00"),
        (3, 103, 120.0, "cancelled", "2026-09-27 12:00:00"),

        (4, 104, 150.0, "completed", "2026-09-28 09:00:00"),
        (5, 105, 90.0, "completed", "2026-09-28 13:00:00"),
        (6, 106, 200.0, "completed", "2026-09-28 15:00:00"),

        (7, 107, 50.0, "completed", "2026-09-29 09:00:00"),
        (8, 108, 70.0, "completed", "2026-09-29 10:00:00"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("status", StringType(), True),
        StructField("order_time", StringType(), True)
    ])

    orders_df = spark.createDataFrame(orders, orders_schema)

    incremental_orders_df = (
        orders_df
        .withColumn(
            "order_time",
            to_timestamp(col("order_time"), "yyyy-MM-dd HH:mm:ss")
        )
        .withColumn(
            "order_date",
            to_date(col("order_time"))
        )
        .filter(
            (col("order_date") == "2026-09-29") &
            (col("customer_id").isNotNull()) &
            (col("amount").isNotNull()) &
            (col("amount") >= 0) &
            (col("status") == "completed")
        )
        .groupBy(col("order_date"))
        .agg(
            count(col("order_id")).alias("total_orders"),
            spark_sum(col("amount")).alias("total_sales"),
            countDistinct(col("customer_id")).alias("unique_customers")
        )
    )

    incremental_orders_df.show()


if __name__ == "__main__":
    main()
