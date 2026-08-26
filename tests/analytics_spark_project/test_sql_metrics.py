from domains.analytics_spark_project.transformations.sql_metrics import (
    build_content_ranking_sql,
    build_daily_active_users_sql,
    build_user_engagement_sql,
)


def test_sql_templates_load_expected_keywords() -> None:
    assert "COUNT(DISTINCT user_id)" in build_daily_active_users_sql()
    assert "GROUP BY user_id" in build_user_engagement_sql()
    assert "category_rank <= 5" in build_content_ranking_sql(top_n=5)
