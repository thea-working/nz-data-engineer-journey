from pyspark.sql import SparkSession


def create_spark():
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("user-activity-pipeline")
        .getOrCreate()
    )

    return spark
