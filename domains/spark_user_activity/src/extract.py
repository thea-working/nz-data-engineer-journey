from pyspark.sql import DataFrame

# extract data from csv file


# extract user logs
def read_user_logs(spark, base_path) -> DataFrame:
    path = base_path / "user_logs.csv"
    return spark.read.csv(str(path), header=True, sep="\t", inferSchema=True)


# extract user profile
def read_user_profile(spark, base_path) -> DataFrame:
    path = base_path / "user_profile.csv"
    return spark.read.csv(str(path), header=True, sep="\t", inferSchema=True)


# extract country info
def read_country_info(spark, base_path) -> DataFrame:
    path = base_path / "country_info.csv"
    return spark.read.csv(str(path), header=True, sep="\t", inferSchema=True)
