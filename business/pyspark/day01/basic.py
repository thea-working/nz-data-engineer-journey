from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *


def main():
    spark = (
        SparkSession.builder
        .appName("dataframe basic")
        .master("local")
        .getOrCreate()
    )

    users = [
        (1, "Alice", 25, "Beijing"),
        (2, "Bob", 30, "Shanghai"),
        (3, "Charlie", 22, "Beijing"),
        (4, "David", 35, "Shenzhen"),
        (5, "Emma", 28, "Shanghai"),
    ]

    schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("city", StringType(), True)
    ])
    # It makes the schema explicit and avoids relying on Spark's schema inference.
    users_df = spark.createDataFrame(users, schema)
    # 输出 DataFrame 的 schema
    users_df.printSchema()

    # 只选择部分列
    users_df.select("user_id", "name", "city").show()

    # 找出age>=28的用户
    users_df.filter(users_df.age >= 28).show()

    # 新增列
    aged_users = (
        users_df.withColumn("age_group",
                            when(col("age") < 30, "young")
                            .otherwise("adult")
                            )
    )
    # select() returns a DataFrame containing the specified columns, while withColumn() adds or replaces a column in the DataFrame.
    aged_users.show()

    result_df = (
        users_df
        .filter((col("city") == "Shanghai") & (col("age") >= 28))
        .withColumn("age_after_5_years", col("age") + 5)
        .select("user_id", "name", "age", "age_after_5_years")
        .orderBy(col("age_after_5_years").desc())
    )
    result_df.show()

    # 找出每个城市的用户数量以及平均年龄。
    avg_df = (
        users_df
        .groupBy(col("city"))
        .agg(
            count(col("user_id")).alias("user_count"),
            avg(col("age")).alias("avg_age")
        )
        .orderBy(col("avg_age").desc())
    )
    avg_df.show()


if __name__ == "__main__":
    main()
