from pathlib import Path

from domains.spark_user_activity.src.spark_session import create_spark


def run_partitions():
    spark = create_spark()
    input_file = Path(__file__).resolve().parent.parent / "data/raw/user_logs.csv"
    df = spark.read.csv(str(input_file), sep="\t", header=True, inferSchema=True)

    print(
        f"df partition number is {df.rdd.getNumPartitions()}",
    )
    df.show()

    df2 = df.repartition(4)
    print(
        f"df2 partition number is {df2.rdd.getNumPartitions()}",
    )
    df2.show()

    df3 = df2.coalesce(1)
    print(
        f"df3 partition number is {df3.rdd.getNumPartitions()}",
    )
    df3.explain()

    df.groupBy("country").count().explain()
    df.coalesce(1).explain()

    df.orderBy("user_id").explain()

    df.repartition(4).rdd.glom().collect()

    spark.stop()


if __name__ == "__main__":
    run_partitions()
