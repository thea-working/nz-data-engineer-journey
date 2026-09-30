from pyspark.core import status
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType
from pyspark.sql.functions import count, sum as spark_sum, countDistinct, col, to_date


def main():
    spark = (
        SparkSession.builder
        .appName("PySpark Optimization")
        .master("local[*]")
        .getOrCreate()
    )

    spark.conf.set("spark.sql.adaptive.enabled", "true")
    orders = [
        (1, 101, 100.0, "Beijing"),
        (2, 102, 80.0, "Shanghai"),
        (3, 101, 50.0, "Beijing"),
        (4, 103, 120.0, "Shenzhen"),
        (5, 101, 70.0, "Beijing"),
        (6, 104, 90.0, "Shanghai"),
        (7, 102, 60.0, "Shanghai"),
        (8, 105, 200.0, "Beijing"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("city", StringType(), True)
    ])

    orders_df = spark.createDataFrame(orders, orders_schema)

    aggregated_df = (
        orders_df.groupBy("city")
        .agg(
            count("order_id").alias("total_orders"),
            spark_sum("amount").alias("total_sales"),
            countDistinct("customer_id").alias("unique_customers")
        )
        .orderBy(col("total_sales").desc())
    )

    # aggregated_df.explain(True)
    aggregated_df.show()

    orders = [
        (1, 101, 100.0, "completed", "Beijing"),
        (2, 102, 80.0, "completed", "Shanghai"),
        (3, 101, 50.0, "cancelled", "Beijing"),
        (4, 103, 120.0, "completed", "Shenzhen"),
        (5, 101, 70.0, "completed", "Beijing"),
        (6, 104, 90.0, "completed", "Shanghai"),
        (7, 102, 60.0, "completed", "Shanghai"),
        (8, 105, 200.0, "completed", "Beijing"),
    ]

    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("status", StringType(), True),
        StructField("city", StringType(), True)
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    cleaned_orders_df = (
        orders_df.filter(
            (col("status") == "completed") &
            (col("amount").isNotNull()) &
            (col("amount") >= 0)
        )
        .select(
            "order_id",
            "customer_id",
            "amount",
            "city"
        )
    )

    cleaned_orders_df.cache()
    cleaned_orders_df.count()

    city_orders_df = (
        cleaned_orders_df
        .groupBy("city")
        .agg(
            count("order_id").alias("total_orders"),
            spark_sum("amount").alias("total_sales")
        )
        .orderBy(col("total_sales").desc())
    )

    aggregated_orders_df = (
        cleaned_orders_df
        .agg(
            countDistinct("customer_id").alias("unique_customers"),
            spark_sum("amount").alias("total_sales")
        )
    )

    city_orders_df.show()
    aggregated_orders_df.show()

    cleaned_orders_df.unpersist()

    orders = [
        (1, 101, 100.0, "completed", "Beijing", "2026-09-28"),
        (2, 102, 80.0, "cancelled", "Shanghai", "2026-09-28"),
        (3, 103, 120.0, "completed", "Shenzhen", "2026-09-29"),
        (4, 101, 50.0, "completed", "Beijing", "2026-09-29"),
        (5, 104, 90.0, "completed", "Shanghai", "2026-09-29"),
        (6, 105, 200.0, "completed", "Beijing", "2026-09-30"),
        (7, 106, 70.0, "completed", "Shanghai", "2026-09-30"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("status", StringType(), True),
        StructField("city", StringType(), True),
        StructField("order_date", StringType(), True)
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    city_aggregated_orders_df = (
        orders_df
        .withColumn(
            "order_date",
            to_date(col("order_date"), "yyyy-MM-dd")
        )
        .filter(
            (col("order_date") == "2026-09-30") &
            (col("status") == "completed")
        )
        .select(
            "city",
            "amount",
            "order_id"
        )
        .groupBy("city")
        .agg(
            count("order_id").alias("total_orders"),
            spark_sum("amount").alias("total_sales")
        )
        .orderBy(col("city"))
    )

    city_aggregated_orders_df.explain(True)
    city_aggregated_orders_df.show()


if __name__ == "__main__":
    main()
