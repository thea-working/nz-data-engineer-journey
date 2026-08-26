from domains.analytics_spark_project.quality.checks import QualityCheck


def test_quality_check_dataclass_fields() -> None:
    check = QualityCheck(
        name="duplicate_event_id_rows",
        passed=True,
        severity="error",
        actual=0,
        expected=0,
        message="duplicate_event_id_rows passed",
    )

    assert check.name == "duplicate_event_id_rows"
    assert check.passed is True
    assert check.actual == check.expected == 0
