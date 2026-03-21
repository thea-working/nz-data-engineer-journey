import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window


def compute_content_ranking(events_df: DataFrame) -> DataFrame:
    """
    Rank content by engagement within each category.
    """
    content_stats = events_df.groupBy("content_id", "category").agg(
        F.count("*").alias("event_count")
    )

    window_spec = Window.partitionBy("category").orderBy(F.desc("event_count"))

    ranked_df = content_stats.withColumn("rank", F.row_number().over(window_spec))
    return ranked_df


def top_n_content(ranked_df: DataFrame, n=10) -> DataFrame:
    """
    get top n content by engagement within each category.
    :param ranked_df: dataframe with rank number
    :param n: top n, default 10
    :return: top n dataframe with category and content_id
    """
    return ranked_df.filter(F.col("rank") <= n)
