from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import col, count, sum as spark_sum, countDistinct, coalesce, lit


def main():
    spark = (
        SparkSession.builder
        .appName("Shenzhen")
        .master("local[*]")
        .getOrCreate()
    )
    orders = [
        (1, 101, 100.0, "Beijing"),
        (2, 102, 80.0, "Shanghai"),
        (3, 101, 50.0, "Beijing"),
        (4, 103, 120.0, "Shenzhen"),
        (5, 104, 90.0, "Shanghai"),
        (6, 102, 60.0, "Shanghai"),
        (7, 105, 200.0, "Beijing"),
        (8, 106, 70.0, "Shanghai"),
        (9, 107, 150.0, "Beijing"),
        (10, 108, 110.0, "Shenzhen"),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("city", StringType(), True)
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    spark.conf.set("spark.sql.shuffle.partitions", "4")
    aggregated_orders_df = (
        orders_df
        .groupBy("city")
        .agg(
            count(col("order_id")).alias("total_orders"),
            coalesce(spark_sum(col("amount")), lit(0)).alias("total_sales"),
            countDistinct(col("customer_id")).alias("unique_customers"),
        )
        .orderBy(col("total_sales").desc())
    )

    aggregated_orders_df.explain(True)
    aggregated_orders_df.show()

    orders = [
        (1, 101, 100.0, "Beijing"),
        (2, 102, 80.0, "Shanghai"),
        (3, 103, 120.0, "Shenzhen"),
        (4, 104, 90.0, "Beijing"),
        (5, 105, 200.0, "Shanghai"),
        (6, 106, 70.0, "Beijing"),
        (7, 107, 150.0, "Shenzhen"),
        (8, 108, 60.0, "Shanghai"),
    ]

    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("city", StringType(), True)
    ])

    orders_df = spark.createDataFrame(orders, orders_schema)
    print("orders_df partitions are: ", orders_df.rdd.getNumPartitions())

    repartition_df = orders_df.repartition(4)
    print("repartition_df partitions are", repartition_df.rdd.getNumPartitions())

    repartition_aggregated_df = (
        repartition_df
        .groupBy("city")
        .agg(
            count(col("order_id")).alias("total_orders"),
            coalesce(spark_sum(col("amount")), lit(0)).alias("total_sales")
        )
        .orderBy("city")
    )

    repartition_aggregated_df.explain(True)
    repartition_aggregated_df.show()

    coalesced_df = orders_df.coalesce(2)
    print("coalesced_df partitions are: ", coalesced_df.rdd.getNumPartitions())

    coalesce_aggregated_df = (
        coalesced_df
        .groupBy("city")
        .agg(
            count(col("order_id")).alias("total_orders"),
            coalesce(spark_sum(col("amount")), lit(0)).alias("total_sales")
        )
        .orderBy("city")
    )

    coalesce_aggregated_df.explain(True)
    coalesce_aggregated_df.show()


if __name__ == "__main__":
    main()
