import logging
from pathlib import Path

from pyspark.sql import SparkSession

from domains.analytics_spark_project.transformations.cleaning import \
    clean_events
from domains.analytics_spark_project.transformations.content_analytics import (
    compute_content_ranking, top_n_content)
from domains.analytics_spark_project.transformations.joins import (
    join_content, join_users)
from domains.analytics_spark_project.transformations.sessionization import (
    aggregate_session_metrics, sessionize)
from domains.analytics_spark_project.transformations.user_analystics import (
    compute_dau, compute_user_metrics)
from domains.analytics_spark_project.utils.io import (read_parquet,
                                                      write_parquet)


def run_pipeline(spark: SparkSession):
    base_dir = Path(__file__).resolve().parent.parent / "data"
    base_dir.mkdir(parents=True, exist_ok=True)
    user_events_file = base_dir / "raw/user_events.parquet"
    user_file = base_dir / "raw/users.parquet"
    content_file = base_dir / "raw/content.parquet"
    cleaned_events_file = base_dir / "silver/cleaned_events.parquet"
    enriched_file = base_dir / "silver/enriched_events.parquet"

    logger = logging.getLogger(__name__)

    # extract data
    logger.info(f"Loading user events from {user_events_file}")
    events = read_parquet(spark, str(user_events_file))
    logger.info(f"Loading user profile from {user_file}")
    users = read_parquet(spark, str(user_file))
    logger.info(f"Loading content from {content_file}")
    content = read_parquet(spark, str(content_file))

    # clean events
    logger.info("Cleaning user events started")
    cleaned_events = clean_events(events)

    # save cleaned events to silver layer
    write_parquet(cleaned_events, str(cleaned_events_file))

    # join users
    logger.info("Join user events, user profile, content started")
    enriched = join_users(cleaned_events, users)

    # join content
    enriched = join_content(enriched, content)

    # save enriched events to sliver layer
    write_parquet(enriched, str(enriched_file))

    # sessionize
    logger.info("Computing session level metrics started")
    sessionized_file = base_dir / "silver/sessionized_events"
    session_metrics_file = base_dir / "gold/session_metrics"

    sessionized = sessionize(enriched)
    write_parquet(sessionized, str(sessionized_file))

    # session metrics
    session_metrics = aggregate_session_metrics(sessionized)
    write_parquet(session_metrics, str(session_metrics_file))

    # user metrics
    logger.info("Computing user level metrics started")
    user_metrics_file = base_dir / "gold/user_metrics"
    user_metrics = compute_user_metrics(session_metrics)
    write_parquet(user_metrics, str(user_metrics_file))

    # dau
    dau_file = base_dir / "gold/dau"
    dau = compute_dau(enriched)
    write_parquet(dau, str(dau_file))

    # content ranking
    logger.info("Computing top N content started")
    top_content_file = base_dir / "gold/content_ranking"
    ranking = compute_content_ranking(enriched)
    top_content = top_n_content(ranking, 10)
    write_parquet(top_content, str(top_content_file))
