WITH content_stats AS (
  SELECT
    category,
    content_id,
    COUNT(*) AS event_count
  FROM enriched_events
  GROUP BY category, content_id
),
ranked AS (
  SELECT
    category,
    content_id,
    event_count,
    ROW_NUMBER() OVER (
      PARTITION BY category
      ORDER BY event_count DESC, content_id ASC
    ) AS category_rank
  FROM content_stats
)
SELECT
  category,
  content_id,
  event_count,
  category_rank
FROM ranked
WHERE category_rank <= {top_n}
