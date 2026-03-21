from pathlib import Path

from domains.spark_user_activity.src.analytics import (country_metrics,
                                                       latest_login)
from domains.spark_user_activity.src.extract import (read_country_info,
                                                     read_user_logs,
                                                     read_user_profile)
from domains.spark_user_activity.src.join import build_enriched_logs
from domains.spark_user_activity.src.spark_session import create_spark
from domains.spark_user_activity.src.transform import (clean_user_logs,
                                                       clean_user_profile)


def run_pipeline():
    spark = create_spark()
    base_path = Path(__file__).resolve().parent.parent / "data/raw"
    output_path = Path(__file__).resolve().parent.parent / "output"

    # extract
    user_logs = read_user_logs(spark, base_path)
    user_profile = read_user_profile(spark, base_path)
    country_info = read_country_info(spark, base_path)

    # clean
    cleaned_user_logs = clean_user_logs(user_logs)
    cleaned_user_profile = clean_user_profile(user_profile)

    # join
    enriched_logs = build_enriched_logs(
        cleaned_user_logs, cleaned_user_profile, country_info
    )

    # analytics
    user_latest_login = latest_login(enriched_logs)

    country_aggregated_metric = country_metrics(enriched_logs)

    # output
    user_latest_login.coalesce(1).write.mode("overwrite").parquet(
        str(output_path / "user_latest_login")
    )
    country_aggregated_metric.write.mode("overwrite").partitionBy("country").parquet(
        str(output_path / "country_metrics")
    )

    # verify
    spark.read.parquet(str(output_path / "user_latest_login")).show()
    spark.read.parquet(str(output_path / "country_metrics")).show()

    spark.stop()


if __name__ == "__main__":
    run_pipeline()
