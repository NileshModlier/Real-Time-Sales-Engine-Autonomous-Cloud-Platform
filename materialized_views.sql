
-- Hourly revenue materialized view
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_hourly_revenue AS
SELECT
  date_trunc('hour', window_start) AS hour,
  SUM(total_revenue) AS revenue
FROM fact_sales_realtime
GROUP BY 1;

-- Fast refresh
CREATE INDEX IF NOT EXISTS idx_mv_hourly_revenue ON mv_hourly_revenue(hour);
