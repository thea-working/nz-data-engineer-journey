import logging
from pathlib import Path

from pyspark.sql import SparkSession

from domains.analytics_spark_project.pipeline.settings import PipelineSettings
from domains.analytics_spark_project.quality.checks import run_quality_checks
from domains.analytics_spark_project.transformations.cleaning import (
    clean_content,
    clean_events,
    clean_users,
)
from domains.analytics_spark_project.transformations.joins import build_enriched_events
from domains.analytics_spark_project.transformations.sessionization import (
    aggregate_session_metrics,
    sessionize,
)
from domains.analytics_spark_project.transformations.sql_metrics import (
    build_content_ranking_sql,
    build_daily_active_users_sql,
    build_user_engagement_sql,
)
from domains.analytics_spark_project.utils.io import (
    read_parquet,
    write_json,
    write_parquet,
)

logger = logging.getLogger(__name__)


def run_pipeline(spark: SparkSession, settings: PipelineSettings | None = None) -> dict:
    settings = settings or PipelineSettings.from_project_root(
        Path(__file__).resolve().parent.parent
    )
    settings.ensure_directories()

    logger.info("Starting analytics pipeline")
    raw_events = read_parquet(spark, settings.raw_events_path)
    raw_users = read_parquet(spark, settings.raw_users_path)
    raw_content = read_parquet(spark, settings.raw_content_path)

    cleaned_events = clean_events(raw_events)
    cleaned_users = clean_users(raw_users)
    cleaned_content = clean_content(raw_content)

    write_parquet(
        cleaned_events, settings.cleaned_events_path, partition_cols=["event_date"]
    )

    enriched_events = build_enriched_events(
        events_df=cleaned_events,
        users_df=cleaned_users,
        content_df=cleaned_content,
    )
    write_parquet(
        enriched_events,
        settings.enriched_events_path,
        partition_cols=["event_date"],
    )

    sessionized_events = sessionize(enriched_events)
    write_parquet(
        sessionized_events,
        settings.sessionized_events_path,
        partition_cols=["event_date"],
    )

    session_metrics = aggregate_session_metrics(sessionized_events)
    write_parquet(
        session_metrics,
        settings.session_metrics_path,
        partition_cols=["session_date"],
    )

    enriched_events.createOrReplaceTempView("enriched_events")
    session_metrics.createOrReplaceTempView("session_metrics")

    daily_active_users = spark.sql(build_daily_active_users_sql())
    write_parquet(
        daily_active_users,
        settings.daily_active_users_path,
        partition_cols=["event_date"],
    )

    user_engagement = spark.sql(build_user_engagement_sql())
    write_parquet(user_engagement, settings.user_engagement_path)

    content_ranking = spark.sql(build_content_ranking_sql(top_n=settings.top_n_content))
    write_parquet(content_ranking, settings.content_ranking_path)

    quality_report = run_quality_checks(
        raw_events_df=raw_events,
        raw_users_df=raw_users,
        raw_content_df=raw_content,
        cleaned_events_df=cleaned_events,
        cleaned_users_df=cleaned_users,
        cleaned_content_df=cleaned_content,
        enriched_events_df=enriched_events,
    )
    write_json(quality_report, settings.quality_report_path)

    summary = {
        "project_root": str(settings.project_root),
        "quality_report_path": settings.quality_report_path,
        "gold_outputs": {
            "daily_active_users": settings.daily_active_users_path,
            "user_engagement": settings.user_engagement_path,
            "content_ranking": settings.content_ranking_path,
            "session_metrics": settings.session_metrics_path,
        },
    }
    logger.info("Analytics pipeline finished successfully")
    return summary
