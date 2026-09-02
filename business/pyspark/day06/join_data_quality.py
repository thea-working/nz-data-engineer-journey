from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *


def main():
    spark = (
        SparkSession.builder
        .appName("JoinDataQuality")
        .master("local")
        .getOrCreate()
    )

    customers = [
        (101, "Alice"),
        (102, "Bob"),
        (103, "Charlie"),
    ]
    customers_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
    ])
    customers_df = spark.createDataFrame(customers, customers_schema)
    orders = [
        (1, 101, 100.0),
        (2, 101, 150.0),
        (3, 102, 200.0),
        (4, 102, 80.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    customer_order_df = (
        customers_df.alias("c").join(
            orders_df.alias("o"),
            col("c.customer_id") == col("o.customer_id"),
            "left")
        .select("c.customer_id",
                "c.name",
                "o.order_id",
                "o.amount"
                )
        .groupBy("customer_id")
        .agg(
            first("name").alias("name"),
            count("order_id").alias("total_orders"),
            coalesce(sum("amount"), lit(0)).alias("total_amount")
        )
    )

    customer_order_df.show()

    customers = [
        (101, "Alice"),
        (102, "Bob"),
        (103, "Charlie"),
        (None, "David"),
    ]
    customers_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
    ])
    customers_df = spark.createDataFrame(customers, customers_schema)

    orders = [
        (1, 101, 100.0),
        (2, 101, 150.0),
        (3, 102, 200.0),
        (4, 102, 80.0),
        (5, 102, 50.0),
        (6, None, 300.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    customer_order_df = (
        customers_df.alias("c").join(
            orders_df.alias("o"),
            col("c.customer_id") == col("o.customer_id"),
            "left")
        .select("c.customer_id",
                "c.name",
                "o.order_id",
                "o.amount"
                )
        .groupBy("customer_id")
        .agg(
            first("name").alias("name"),
            count("order_id").alias("total_orders"),
            coalesce(sum("amount"), lit(0)).alias("total_amount")
        )
        .orderBy("customer_id")
    )
    customer_order_df.show()

    customers = [
        (101, "Alice"),
        (102, "Bob"),
        (103, "Charlie"),
    ]
    customers_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
    ])
    customers_df = spark.createDataFrame(customers, customers_schema)

    orders = [
        (1, 101, 1, 100.0),
        (2, 101, 2, 150.0),
        (3, 102, 2, 200.0),
        (4, 102, 3, 80.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    products = [
        (1, "Laptop"),
        (2, "Phone"),
        (3, "Tablet"),
    ]
    products_schema = StructType([
        StructField("product_id", IntegerType(), True),
        StructField("product_name", StringType(), True)
    ])
    products_df = spark.createDataFrame(products, products_schema)

    customer_order_products_df = (
        customers_df.alias("c").join(
            orders_df.alias("o"),
            col("c.customer_id") == col("o.customer_id"),
            "left"
        ).select(
            "c.customer_id",
            "c.name",
            "o.order_id",
            "o.product_id",
            "o.amount"
        ).alias("t")
        .join(
            products_df.alias("p"),
            col("t.product_id") == col("p.product_id"),
            "left"
        ).select(
            "customer_id",
            "name",
            "order_id",
            "amount",
            "t.product_id",
            "p.product_name"
        )
        .groupBy("customer_id")
        .agg(
            first("name").alias("name"),
            count("order_id").alias("total_orders"),
            coalesce(sum("amount"), lit(0)).alias("total_amount"),
            count_distinct("product_id").alias("distinct_products")
        )
        .orderBy("customer_id")
    )

    customer_order_products_df.show()


if __name__ == "__main__":
    main()
