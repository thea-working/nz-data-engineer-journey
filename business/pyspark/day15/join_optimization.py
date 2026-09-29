from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col, count, sum as spark_sum, coalesce, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType


def main():
    spark = (
        SparkSession.builder
        .appName("Join optimization")
        .master("local[*]")
        .getOrCreate()
    )
    orders = [
        (1, 101, 100.0),
        (2, 102, 80.0),
        (3, 103, 120.0),
        (4, 101, 50.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True)
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    customers = [
        (101, "Alice", "Beijing"),
        (102, "Bob", "Shanghai"),
        (103, "Charlie", "Shenzhen"),
    ]
    customer_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True)
    ])
    customer_df = spark.createDataFrame(customers, customer_schema)

    order_with_customer = (
        orders_df.alias("o").join(
            broadcast(customer_df).alias("c"),
            col("o.customer_id") == col("c.customer_id")
        )
        .select(
            col("o.order_id").alias("order_id"),
            col("o.customer_id").alias("customer_id"),
            col("c.name").alias("name"),
            col("c.city").alias("city"),
            col("o.amount").alias("amount")
        )
        .orderBy("order_id")
    )

    order_with_customer.show()

    customers = [
        (101, "Alice"),
        (102, "Bob"),
    ]
    customer_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    customer_df = spark.createDataFrame(customers, customer_schema)

    orders = [
        (1, 101, 100.0),
        (2, 101, 80.0),
        (3, 101, 50.0),
        (4, 102, 120.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True)
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    customers_order_count_df = (
        customer_df.alias("c").join(
            orders_df.alias("o"),
            col("c.customer_id") == col("o.customer_id"),
            "left"
        )
        .groupBy("c.customer_id", "c.name")
        .agg(
            count(col("o.order_id")).alias("order_count"),
            coalesce(spark_sum(col("o.amount")), lit(0)).alias("total_sales")
        )
    )

    customers_order_count_df.show()

    orders = [
        (1, 101, 100.0),
        (2, 102, 80.0),
        (3, 103, 120.0),
        (4, 101, 50.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True)
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    customers = [
        (101, "Alice", "Beijing"),
        (102, "Bob", "Shanghai"),
        (103, "Charlie", "Shenzhen"),
    ]
    customer_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True)
    ])
    customer_df = spark.createDataFrame(customers, customer_schema)

    city_aggregated_df = (
        orders_df.alias("o").join(
            broadcast(customer_df).alias("c"),
            col("o.customer_id") == col("c.customer_id")
        )
        .groupBy("c.city")
        .agg(
            count(col("o.order_id")).alias("total_orders"),
            coalesce(spark_sum(col("o.amount")), lit(0)).alias("total_sales")
        )
        .orderBy("c.city")
    )
    city_aggregated_df.show()


if __name__ == "__main__":
    main()
