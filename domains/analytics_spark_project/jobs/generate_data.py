import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

from pyspark.sql import Row

from domains.analytics_spark_project.pipeline.settings import PipelineSettings
from domains.analytics_spark_project.utils.spark_session import create_spark


def _build_event_rows(
    user_ids: list[str],
    content_ids: list[str],
    countries: list[str],
    devices: list[str],
    event_types: list[str],
    start_time: datetime,
    event_count: int,
) -> list[Row]:
    return [
        Row(
            event_id=f"e{i}",
            user_id=random.choice(user_ids),
            content_id=random.choice(content_ids),
            event_type=random.choice(event_types),
            device=random.choice(devices),
            country=random.choice(countries),
            event_time=start_time + timedelta(minutes=random.randint(0, 7 * 24 * 60)),
        )
        for i in range(event_count)
    ]


def _build_user_rows(
    user_ids: list[str], countries: list[str], start_time: datetime
) -> list[Row]:
    return [
        Row(
            user_id=user_id,
            age=random.randint(18, 65),
            signup_country=random.choice(countries),
            signup_date=(start_time - timedelta(days=random.randint(30, 365))).date(),
        )
        for user_id in user_ids
    ]


def _build_content_rows(
    content_ids: list[str], categories: list[str], start_time: datetime
) -> list[Row]:
    return [
        Row(
            content_id=content_id,
            category=random.choice(categories),
            author_id=f"a{random.randint(1, 500)}",
            publish_time=start_time - timedelta(days=random.randint(1, 180)),
        )
        for content_id in content_ids
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate sample parquet datasets for the analytics project"
    )
    parser.add_argument("--event-count", type=int, default=100000)
    parser.add_argument("--user-count", type=int, default=5000)
    parser.add_argument("--content-count", type=int, default=500)
    return parser.parse_args()


def create_data(event_count: int, user_count: int, content_count: int) -> None:
    spark = create_spark(app_name="user-behavior-analytics-data-generator")
    project_root = Path(__file__).resolve().parent.parent
    settings = PipelineSettings.from_project_root(project_root)
    settings.ensure_directories()

    user_ids = [f"u{i}" for i in range(1, user_count + 1)]
    content_ids = [f"c{i}" for i in range(1, content_count + 1)]
    countries = ["US", "UK", "CN", "NZ", "AU"]
    devices = ["android", "ios", "web"]
    event_types = ["view"] * 6 + ["like", "comment", "share", "login", "logout"]
    categories = ["sports", "tech", "finance", "music", "gaming"]
    start_time = datetime(2026, 1, 1, 0, 0, 0)

    events_df = spark.createDataFrame(
        _build_event_rows(
            user_ids=user_ids,
            content_ids=content_ids,
            countries=countries,
            devices=devices,
            event_types=event_types,
            start_time=start_time,
            event_count=event_count,
        )
    ).repartition(8)
    users_df = spark.createDataFrame(_build_user_rows(user_ids, countries, start_time))
    content_df = spark.createDataFrame(
        _build_content_rows(content_ids, categories, start_time)
    )

    events_df.write.mode("overwrite").parquet(settings.raw_events_path)
    users_df.write.mode("overwrite").parquet(settings.raw_users_path)
    content_df.write.mode("overwrite").parquet(settings.raw_content_path)
    spark.stop()


if __name__ == "__main__":
    arguments = parse_args()
    create_data(
        event_count=arguments.event_count,
        user_count=arguments.user_count,
        content_count=arguments.content_count,
    )
