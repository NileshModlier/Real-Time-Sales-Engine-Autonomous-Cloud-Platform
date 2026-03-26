
-- Fact table for real-time aggregated sales
CREATE TABLE IF NOT EXISTS fact_sales_realtime (
  window_start TIMESTAMP NOT NULL,
  window_end TIMESTAMP NOT NULL,
  store_location TEXT NOT NULL,
  total_orders INT NOT NULL,
  total_quantity INT NOT NULL,
  total_revenue NUMERIC NOT NULL
);

-- Indexes for fast Power BI querying
CREATE INDEX IF NOT EXISTS idx_sales_window ON fact_sales_realtime(window_start, window_end);
CREATE INDEX IF NOT EXISTS idx_sales_location ON fact_sales_realtime(store_location);
