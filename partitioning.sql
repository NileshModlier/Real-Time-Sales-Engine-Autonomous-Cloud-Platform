
-- Example partitioning strategy
ALTER TABLE fact_sales_realtime
  PARTITION BY RANGE (window_start);

CREATE TABLE IF NOT EXISTS fact_sales_2026_q1
  PARTITION OF fact_sales_realtime
  FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');
