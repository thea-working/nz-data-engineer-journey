from pathlib import Path

from domains.spark_user_activity.src.spark_session import create_spark


def run_execution():
    spark = create_spark()
    input_file = Path(__file__).resolve().parent.parent / "data/raw/user_logs.csv"
    df = spark.read.csv(str(input_file), sep="\t", header=True, inferSchema=True)

    df.cache()

    df2 = df.filter("country = 'US'")
    df3 = df2.groupBy("country").count()
    df3.show()
    df3.explain(True)

    df.filter("country = 'US'").select("user_id").explain()
    print(df.count())

    spark.stop()


if __name__ == "__main__":
    run_execution()
