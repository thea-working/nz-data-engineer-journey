from pyspark.sql import SparkSession, Window
from pyspark.sql.types import IntegerType, DoubleType, StructType, StructField, StringType
from pyspark.sql.functions import col, when, sum, lit, to_date, count


def main():
    spark = (
        SparkSession.builder
        .appName("PySpark Data Quality")
        .master("local[*]")
        .getOrCreate()
    )

    orders = [
        (1, 101, 100.0, "2026-09-01"),
        (2, 102, 50.0, "2026-09-01"),
        (3, None, 80.0, "2026-09-02"),
        (4, 103, None, "2026-09-02"),
        (5, 104, -20.0, "2026-09-03"),
        (5, 105, 120.0, "2026-09-03"),
        (6, 106, 200.0, None),
        (7, None, None, None),
    ]

    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("order_date", StringType(), True),
    ])

    orders_df = spark.createDataFrame(orders, orders_schema)

    # 输出 NULL customer_id 的记录数量。
    null_id_count = orders_df.filter(col("customer_id").isNull()).count()
    print("Null customer_id count: ", null_id_count)

    # 输出 NULL amount 的记录数量。
    null_amount_count = orders_df.filter(col("amount").isNull()).count()
    print("Null amount count: ", null_amount_count)

    # amount < 0 就是非法数据
    invalid_amount_count = orders_df.filter(col("amount") < 0).count()
    print("Invalid amount count: ", invalid_amount_count)

    # 检查重复的 order_id
    order_count_df = (
        orders_df
        .groupBy(col("order_id"))
        .count()
        .filter(col("count") >= 2)
    )
    order_count_df.show()

    orders = [
        (1, 101, 100.0, "2026-09-01"),
        (2, 102, 50.0, "2026-09-01"),
        (3, None, 80.0, "2026-09-02"),
        (4, 103, None, "2026-09-02"),
        (5, 104, -20.0, "2026-09-03"),
        (5, 105, 120.0, "2026-09-03"),
        (6, 106, 200.0, None),
        (7, None, None, None),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("order_date", StringType(), True),
    ])

    orders_df = spark.createDataFrame(orders, orders_schema)

    check_valid_orders = (
        orders_df
        .withColumn(
            "quality_status",
            when((col("customer_id").isNotNull())
                 & (col("amount").isNotNull())
                 & (col("amount") >= 0)
                 & (col("order_date").isNotNull()),
                 lit("valid")
                 ).otherwise(lit("invalid"))
        )
    )

    valid_orders = check_valid_orders.filter(col("quality_status") == "valid")
    print("Valid records: ", valid_orders.count())
    invalid_orders = check_valid_orders.filter(col("quality_status") == "invalid")
    print("Invalid records: ", invalid_orders.count())

    valid_amount = (
        check_valid_orders
        .filter(col("quality_status") == "valid")
        .agg(sum(col("amount")).alias("valid_amount"))
    )
    valid_amount.show()

    orders = [
        (1, 101, 100.0, 2, "completed", "2026-09-01"),
        (2, 102, 50.0, 3, "completed", "2026-09-01"),
        (3, None, 80.0, 2, "completed", "2026-09-02"),
        (4, 103, None, 1, "completed", "2026-09-02"),
        (5, 104, -20.0, 1, "completed", "2026-09-03"),
        (6, 105, 120.0, None, "completed", "2026-09-03"),
        (7, 106, 200.0, 1, "cancelled", "2026-09-04"),
        (8, 107, 80.0, 2, None, "2026-09-04"),
        (9, 108, 60.0, 2, "completed", None),
        (9, 109, 100.0, 1, "completed", "2026-09-05"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("status", StringType(), True),
        StructField("order_date", StringType(), True),
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)
    # status = "completed"
    # customer_id 不为 NULL
    # unit_price 不为 NULL 且 unit_price >= 0
    # quantity 不为 NULL 且 quantity > 0
    # order_date 不为 NULL
    # order_date: String → DateType
    # total_amount = unit_price * quantity
    check_null_orders = (
        orders_df
        .withColumn(
            "quality_status",
            when(
                (col("status") == "completed")
                & (col("customer_id").isNotNull())
                & (col("unit_price").isNotNull())
                & (col("unit_price") >= 0)
                & (col("quantity").isNotNull())
                & (col("quantity") > 0)
                & (col("order_date").isNotNull()),
                lit("valid")
            ).otherwise(lit("invalid"))
        )
        .withColumn(
            "order_date",
            to_date(col("order_date"), "yyyy-MM-dd"),
        )
        .withColumn(
            "total_amount",
            col("unit_price") * col("quantity")
        )
    )

    window = Window.partitionBy("order_id")
    check_duplicate_orders = (
        check_null_orders
        .withColumn(
            "quality_status",
            when(
                count("*").over(window) > 1,
                lit("invalid")
            ).otherwise(col("quality_status"))
        )
    )

    check_duplicate_orders.filter(col("quality_status") == "valid").show()
    check_duplicate_orders.filter(col("quality_status") == "invalid").show()

    total_orders = (
        check_duplicate_orders
        .filter(col("quality_status") == "valid")
        .agg(count(col("order_id")).alias("total_orders"),
             sum(col("total_amount")).alias("total_amount")
             )
    )
    total_orders.show()


if __name__ == "__main__":
    main()
