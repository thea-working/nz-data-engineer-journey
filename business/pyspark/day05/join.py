from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def main():
    spark = (
        SparkSession.builder
        .appName("Join")
        .master("local")
        .getOrCreate()
    )
    users = [
        (101, "Alice", "Beijing"),
        (102, "Bob", "Shanghai"),
        (103, "Charlie", "Shenzhen"),
        (104, "David", "Beijing"),
    ]
    user_schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
    ])
    users_df = spark.createDataFrame(users, user_schema)

    orders = [
        (1, 101, 100.0),
        (2, 101, 150.0),
        (3, 102, 200.0),
        (4, 103, 80.0),
        (5, 105, 300.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    # 保留所有用户，并关联他们的订单。
    user_orders = users_df.join(
        orders_df,
        users_df.user_id == orders_df.user_id,
        "left"
    ).select(
        users_df.user_id,
        "name",
        "city",
        "order_id",
        "amount"
    )
    user_orders.show()

    # 计算每个用户的订单总金额。
    user_total_orders = (
        users_df.alias("u").join(
            orders_df.alias("o"),
            col("u.user_id") == col("o.user_id"),
            "left"
        ).select(
            "u.user_id",
            "name",
            "order_id",
            "amount"
        ).groupBy("user_id")
        .agg(
            first("name").alias("name"),
            count("order_id").alias("total_orders"),
            coalesce(sum("amount"), lit(0)).alias("total_amount")
        ))
    user_total_orders.show()

    # broadcast join
    user_orders_df = orders_df.alias("o").join(
        broadcast(users_df.alias("u")),
        col("o.user_id") == col("u.user_id"),
    ).select(
        "u.user_id",
        "name",
        "city",
        "order_id",
        "amount"
    )
    user_orders_df.show()


if __name__ == "__main__":
    main()
