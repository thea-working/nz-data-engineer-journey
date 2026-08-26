from dataclasses import asdict, dataclass

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from domains.analytics_spark_project.transformations.cleaning import ALLOWED_EVENT_TYPES


@dataclass(frozen=True)
class QualityCheck:
    name: str
    passed: bool
    severity: str
    actual: int
    expected: int
    message: str


def _make_check(
    name: str,
    actual: int,
    expected: int = 0,
    severity: str = "error",
    success_message: str | None = None,
    failure_message: str | None = None,
) -> QualityCheck:
    passed = actual == expected
    if passed:
        message = success_message or f"{name} passed"
    else:
        message = (
            failure_message
            or f"{name} failed with actual={actual}, expected={expected}"
        )
    return QualityCheck(
        name=name,
        passed=passed,
        severity=severity,
        actual=actual,
        expected=expected,
        message=message,
    )


def _duplicate_key_count(df: DataFrame, key: str) -> int:
    duplicate_rows = (
        df.groupBy(key)
        .count()
        .filter(F.col("count") > 1)
        .agg(F.sum("count"))
        .first()[0]
    )
    return int(duplicate_rows or 0)


def run_quality_checks(
    raw_events_df: DataFrame,
    raw_users_df: DataFrame,
    raw_content_df: DataFrame,
    cleaned_events_df: DataFrame,
    cleaned_users_df: DataFrame,
    cleaned_content_df: DataFrame,
    enriched_events_df: DataFrame,
) -> dict:
    raw_event_count = raw_events_df.count()
    cleaned_event_count = cleaned_events_df.count()
    raw_user_count = raw_users_df.count()
    cleaned_user_count = cleaned_users_df.count()
    raw_content_count = raw_content_df.count()
    cleaned_content_count = cleaned_content_df.count()

    invalid_event_type_count = raw_events_df.filter(
        ~F.col("event_type").isin(ALLOWED_EVENT_TYPES)
    ).count()
    invalid_event_time_count = (
        raw_events_df.withColumn("parsed_event_time", F.to_timestamp("event_time"))
        .filter(F.col("parsed_event_time").isNull())
        .count()
    )
    invalid_user_age_count = raw_users_df.filter(
        (F.col("age").cast("int") < 13) | (F.col("age").cast("int") > 100)
    ).count()
    duplicate_event_id_count = _duplicate_key_count(raw_events_df, "event_id")
    duplicate_user_id_count = _duplicate_key_count(raw_users_df, "user_id")
    duplicate_content_id_count = _duplicate_key_count(raw_content_df, "content_id")
    orphan_user_events_count = enriched_events_df.filter(
        F.col("signup_country").isNull()
    ).count()
    orphan_content_events_count = enriched_events_df.filter(
        F.col("category").isNull()
    ).count()

    checks = [
        _make_check(
            "invalid_event_types",
            invalid_event_type_count,
            failure_message="Raw events contain unsupported event types",
        ),
        _make_check(
            "unparseable_event_timestamps",
            invalid_event_time_count,
            failure_message="Raw events contain timestamps that could not be parsed",
        ),
        _make_check(
            "invalid_user_age_range",
            invalid_user_age_count,
            failure_message="Raw users contain ages outside the accepted range 13-100",
        ),
        _make_check(
            "duplicate_event_id_rows",
            duplicate_event_id_count,
            failure_message="Raw events contain duplicate event_id rows",
        ),
        _make_check(
            "duplicate_user_id_rows",
            duplicate_user_id_count,
            failure_message="Raw users contain duplicate user_id rows",
        ),
        _make_check(
            "duplicate_content_id_rows",
            duplicate_content_id_count,
            failure_message="Raw content contains duplicate content_id rows",
        ),
        _make_check(
            "orphan_user_references",
            orphan_user_events_count,
            severity="warn",
            failure_message=(
                "Enriched events still contain user_ids "
                "missing from the user dimension"
            ),
        ),
        _make_check(
            "orphan_content_references",
            orphan_content_events_count,
            severity="warn",
            failure_message=(
                "Enriched events still contain content_ids "
                "missing from the content dimension"
            ),
        ),
    ]

    return {
        "datasets": {
            "raw_events": raw_event_count,
            "cleaned_events": cleaned_event_count,
            "raw_users": raw_user_count,
            "cleaned_users": cleaned_user_count,
            "raw_content": raw_content_count,
            "cleaned_content": cleaned_content_count,
        },
        "quality_gate_passed": all(
            check.passed or check.severity == "warn" for check in checks
        ),
        "checks": [asdict(check) for check in checks],
    }
