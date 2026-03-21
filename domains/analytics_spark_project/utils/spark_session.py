from pyspark.sql import SparkSession


def create_spark() -> SparkSession:
    spark = (
        SparkSession.builder.appName("analytics_spark_project")
        .master("local[6]")
        .config("spark.sql.shuffle.partitions", 32)
        .config("spark.default.parallelism", 32)
        .config("spark.driver.memory", "4g")
        .getOrCreate()
    )
    return spark
