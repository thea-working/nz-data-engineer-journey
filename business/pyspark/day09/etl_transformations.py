from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *


def main():
    spark = (
        SparkSession.builder
        .appName("etl_transformations")
        .master("local[*]")
        .getOrCreate())

    users = [
        (1, " Alice ", "BEIJING", 25, "2026-09-01"),
        (2, "Bob", " shanghai ", None, "2026-09-02"),
        (3, "  CHARLIE", None, 30, None),
        (4, "David ", "SHENZHEN", -1, "2026-09-03"),
        (5, None, "beijing", 28, "2026-09-04"),
    ]
    users_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("event_date", StringType(), True),
    ])
    users_df = spark.createDataFrame(users, users_schema)

    cleaned_df = users_df.withColumn(
        "name",
        lower(trim(col("name")))
    )

    cleaned_df = cleaned_df.withColumn(
        "city",
        lower(trim(col("city")))
    )

    cleaned_df = cleaned_df.withColumn(
        "age",
        when(col("age") < 0, None)
        .otherwise(col("age"))
    )

    cleaned_df = cleaned_df.withColumn(
        "event_date",
        to_date(col("event_date"))
    )

    cleaned_df.printSchema()
    cleaned_df.show()

    orders = [
        (1, 101, 100.0, 2, "completed"),
        (2, 101, 50.0, 3, "completed"),
        (3, 102, 200.0, 1, "cancelled"),
        (4, 103, None, 2, "completed"),
        (5, 102, 80.0, 4, "completed"),
        (6, 104, -20.0, 1, "completed"),
        (7, 105, 120.0, None, "completed"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("status", StringType(), True)
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)
    # 构建一个 cleaned_orders_df：
    #
    # 只保留 status = "completed" 的订单
    # unit_price 为 NULL 的订单过滤掉
    # quantity 为 NULL 或 <= 0 的订单过滤掉
    # unit_price 为负数的订单过滤掉
    # 新增：
    # total_amount = unit_price * quantity
    # 最终只保留：
    # order_id
    # customer_id
    # unit_price
    # quantity
    # total_amount
    cleaned_orders_df = (
        orders_df.filter(
            (col("status") == "completed") &
            (col("unit_price").isNotNull()) &
            (col("unit_price") >= 0) &
            (col("quantity").isNotNull()) &
            (col("quantity") > 0)
        ).withColumn(
            "total_amount",
            round(col("unit_price") * col("quantity"), 2)
        ).select(
            "order_id",
            "customer_id",
            "unit_price",
            "quantity",
            "total_amount"
        )
    )

    cleaned_orders_df.show()

    customers = [
        (101, "Alice", "Beijing"),
        (102, "Bob", "Shanghai"),
        (103, "Charlie", "Beijing"),
        (104, "David", "Shenzhen"),
    ]
    customers_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True)
    ])
    customers_df = spark.createDataFrame(customers, customers_schema)

    orders = [
        (1, 101, 100.0, 2, "completed", "2026-09-01"),
        (2, 101, 50.0, 3, "completed", "2026-09-02"),
        (3, 102, 200.0, 1, "cancelled", "2026-09-02"),
        (4, 103, 80.0, 2, "completed", "2026-09-03"),
        (5, 102, 80.0, 4, "completed", "2026-09-03"),
        (6, 104, 120.0, 1, "completed", "2026-09-04"),
        (7, 101, 60.0, 2, "completed", "2026-09-05"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("status", StringType(), True),
        StructField("order_date", StringType(), True)
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)
    cleaned_orders_df = (
        orders_df.filter(
            (col("status") == "completed") &
            (col("unit_price").isNotNull()) &
            (col("unit_price") >= 0) &
            (col("quantity").isNotNull()) &
            (col("quantity") > 0)
        ).withColumn(
            "order_date",
            to_date(col("order_date"))
        ).withColumn(
            "total_amount",
            col("unit_price") * col("quantity")
        ).select(
            "order_id",
            "customer_id",
            "unit_price",
            "quantity",
            "order_date",
            "total_amount"
        )
    )

    city_orders = (
        customers_df.alias("c").join(
            cleaned_orders_df.alias("o"),
            col("c.customer_id") == col("o.customer_id")
        ).select(
            col("c.city").alias("city"),
            col("o.customer_id").alias("customer_id"),
            col("o.order_id").alias("order_id"),
            col("o.total_amount").alias("total_amount")
        )
        .groupBy("city")
        .agg(
            count_distinct(col("customer_id")).alias("total_customers"),
            count(col("order_id")).alias("total_orders"),
            sum(col("total_amount")).alias("total_sales")
        )
    )

    city_orders.show()


if __name__ == '__main__':
    main()
