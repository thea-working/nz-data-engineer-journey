import random
from datetime import datetime, timedelta
from pathlib import Path

from pyspark.sql import Row

from domains.analytics_spark_project.utils.spark_session import create_spark


def create_data():
    base_dir = Path(__file__).resolve().parent.parent / "data/raw"
    base_dir.mkdir(parents=True, exist_ok=True)
    spark = create_spark()

    users = [f"u{i}" for i in range(1, 5001)]
    contents = [f"c{i}" for i in range(1, 501)]
    countries = ["US", "UK", "CN", "NZ", "AU"]
    devices = ["android", "ios", "web"]
    events = (
        ["view"] * 5
        + ["like"] * 1
        + ["comment"] * 1
        + ["share"] * 1
        + ["login"] * 1
        + ["logout"] * 1
    )

    categories = ["sports", "tech", "news", "music", "gaming"]

    # generate events dataset
    rows = []
    start = datetime(2026, 3, 1)
    for i in range(500000):
        row = Row(
            event_id=i,
            user_id=random.choice(users),
            event_type=random.choice(events),
            content_id=random.choice(contents),
            device=random.choice(devices),
            country=random.choice(countries),
            event_time=start + timedelta(minutes=random.randint(0, 5000)),
        )
        rows.append(row)
    df = spark.createDataFrame(rows).repartition(32)
    df.write.mode("overwrite").parquet(str(base_dir / "user_events.parquet"))

    # generate users dataset
    user_rows = []
    for u in users:
        user_rows.append(
            Row(
                user_id=u,
                age=random.randint(18, 60),
                signup_country=random.choice(countries),
                signup_date=start - timedelta(days=random.randint(0, 365)),
            )
        )

        users_df = spark.createDataFrame(user_rows).repartition(32)
        users_df.write.mode("overwrite").parquet(str(base_dir / "users.parquet"))

    # generate content dataset
    content_rows = []
    for c in contents:
        content_rows.append(
            Row(
                content_id=c,
                category=random.choice(categories),
                author_id=f"a{random.randint(1, 200)}",
                publish_time=start - timedelta(days=random.randint(0, 180)),
            )
        )
    content_df = spark.createDataFrame(content_rows).repartition(6)
    content_df.write.mode("overwrite").parquet(str(base_dir / "content.parquet"))

    spark.stop()


if __name__ == "__main__":
    create_data()
