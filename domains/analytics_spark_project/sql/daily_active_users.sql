SELECT
  event_date,
  COUNT(DISTINCT user_id) AS daily_active_users
FROM enriched_events
GROUP BY event_date
