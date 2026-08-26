SELECT
  user_id,
  COUNT(DISTINCT session_id) AS session_count,
  ROUND(AVG(session_duration_seconds), 2) AS avg_session_duration_seconds,
  SUM(event_count) AS event_count
FROM session_metrics
GROUP BY user_id
