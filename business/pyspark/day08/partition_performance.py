from pyspark.sql import SparkSession
from pyspark.sql.types import *


def main():
    spark = (
        SparkSession.builder
        .appName("PythonPartitionPerformance")
        .master("local[*]")
        .getOrCreate()
    )
    orders = [
        (1, 101, 100.0),
        (2, 102, 150.0),
        (3, 101, 200.0),
        (4, 103, 80.0),
        (5, 102, 120.0),
        (6, 101, 300.0),
        (7, 103, 90.0),
        (8, 102, 180.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)
    print(orders_df.rdd.getNumPartitions())

    repartitioned_df = orders_df.repartition(4)
    print(repartitioned_df.rdd.getNumPartitions())

    coalesce_df = repartitioned_df.coalesce(2)
    print(coalesce_df.rdd.getNumPartitions())

    orders = [
        (1, 101, 100.0),
        (2, 101, 150.0),
        (3, 101, 200.0),
        (4, 101, 80.0),
        (5, 101, 120.0),
        (6, 101, 300.0),
        (7, 101, 90.0),
        (8, 102, 100.0),
        (9, 103, 200.0),
        (10, 104, 150.0),
    ]
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
    ])
    orders_df = spark.createDataFrame(orders, orders_schema)

    result = (
        orders_df
        .groupBy("customer_id")
        .sum("amount")
    )

    result.show()


if __name__ == "__main__":
    main()
