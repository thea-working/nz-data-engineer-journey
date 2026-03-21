from pyspark.sql import DataFrame, SparkSession


def read_parquet(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.parquet(path)


def write_parquet(df: DataFrame, path: str, partition_cols=None) -> None:
    writer = df.write.mode("overwrite")
    if partition_cols:
        writer = writer.partitionBy(*partition_cols)

    writer.parquet(path)
