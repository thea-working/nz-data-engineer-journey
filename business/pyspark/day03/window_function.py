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
        (1, 101, 100.0, "2026-08-28 10:00:00"),
        (2, 101, 150.0, "2026-08-28 11:00:00"),
        (3, 102, 200.0, "2026-08-28 09:00:00"),
        (4, 102, 300.0, "2026-08-28 12:00:00"),
        (5, 103, 120.0, "2026-08-28 08:00:00"),
        (6, 103, 180.0, "2026-08-28 13:00:00"),
    ]

    schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("amount", DoubleType(), True),
        StructField("event_time", StringType(), True),
    ])

    orders_df = spark.createDataFrame(orders, schema)
    # Find the latest order for each user.
    user_latest_order = (
        orders_df.withColumn(
            "row_num",
            row_number().over(
                Window.partitionBy("user_id")
                .orderBy(col("event_time").desc())
            )
        ).filter(col("row_num") == 1)
        .select("user_id", "order_id", "amount", "event_time")
    )
    user_latest_order.show()

    sales = [
        (1, "Beijing", "Alice", 1000.0),
        (2, "Beijing", "Bob", 1500.0),
        (3, "Beijing", "Charlie", 1200.0),
        (4, "Shanghai", "David", 2000.0),
        (5, "Shanghai", "Emma", 1800.0),
        (6, "Shanghai", "Frank", 2200.0),
        (7, "Shenzhen", "Grace", 1600.0),
        (8, "Shenzhen", "Helen", 1400.0),
    ]
    sales_schema = StructType([
        StructField("sale_id", IntegerType(), True),
        StructField("city", StringType(), True),
        StructField("salesperson", StringType(), True),
        StructField("amount", DoubleType(), True),
    ])
    sales_df = spark.createDataFrame(sales, schema=sales_schema)
    # 找出每个城市销售额最高的 2 条记录。
    city_top_sales = (
        sales_df.withColumn(
            "row_num",
            row_number().over(
                Window.partitionBy("city")
                .orderBy(col("amount").desc())
            )
        )
        .filter(col("row_num") <= 2)
        .select("city", "salesperson", "amount")
    )
    city_top_sales.show()

    employees = [
        (1, "Alice", "Engineering", 120000.0),
        (2, "Bob", "Engineering", 120000.0),
        (3, "Charlie", "Engineering", 100000.0),
        (4, "David", "Sales", 90000.0),
        (5, "Emma", "Sales", 90000.0),
        (6, "Frank", "Sales", 80000.0),
    ]
    employees_schema = StructType([
        StructField("employee_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("department", StringType(), True),
        StructField("salary", DoubleType(), True),
    ])
    employees_df = spark.createDataFrame(employees, schema=employees_schema)
    # 找出每个部门薪资最高的员工。如果最高薪资有并列，需要把所有并列第一的员工都保留下来。
    top_salary_employees = (
        employees_df.withColumn(
            "rank",
            rank().over(
                Window.partitionBy("department")
                .orderBy(col("salary").desc())
            )
        )
        .filter(col("rank") == 1)
        .select("department", "name", "salary", "rank")
    )
    top_salary_employees.show()


if __name__ == "__main__":
    main()
