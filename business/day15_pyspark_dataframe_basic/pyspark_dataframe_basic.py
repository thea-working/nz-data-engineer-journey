from pyspark.sql import SparkSession
from pyspark.sql.types import DecimalType


def main():
    # output_path = Path(__file__).resolve().parent.parent / "data/filtered_users.csv"
    # create SparkSession
    spark = (
        SparkSession.builder.appName("PySpark Dataframe Basic")
        .master("local")
        .getOrCreate()
    )

    # create simple dataframe
    data = [
        (1, "Alice", 19, "US", 160),
        (2, "Bob", 24, "UK", 200),
        (3, "Mike", 18, "NZ", 240),
        (7, "Mike", 19, "NZ", 250),
        (4, "Eleven", 18, "NZ", 360),
        (5, "Max", 20, "AU", 180),
        (6, "Will", 21, "US", 210),
    ]
    columns = ["user_id", "name", "age", "country", "amount"]
    df = spark.createDataFrame(data, columns)

    df.printSchema()
    df.show()

    # filter rows
    df_filtered = df.filter(df.amount > 200)
    df_filtered.show()

    # add new column
    df_new = df_filtered.withColumn(
        "amount_with_tax", (df_filtered.amount * 1.1).cast(DecimalType(10, 2))
    )
    df_new.show()

    # remove duplicates
    df_unique = df_new.dropDuplicates(["name"])
    df_unique.show()

    # sort by amount
    df_sorted = df_unique.orderBy(df_unique.amount_with_tax.desc())
    df_sorted.show()

    # read / write csv file
    # df_sorted.write.csv(str(output_path), mode='overwrite', header=True)
    #
    # df_read = spark.read.csv(str(output_path), header=True, inferSchema=True)
    # df_read.show()


if __name__ == "__main__":
    main()
