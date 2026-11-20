-- Sales Performance Intelligence
-- SQL dialect: SQLite
-- Import datasets/sales_data.csv into a table named sales_data first.
-- All monetary values are in unspecified currency units.

-- 1. Inspect the dataset
SELECT *
FROM sales_data
LIMIT 10;

-- 2. Check row count and distinct orders
SELECT
    COUNT(*) AS order_lines,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales_data;

-- 3. Overall performance KPIs
SELECT
    SUM(quantity * unit_price) AS total_revenue,
    SUM(quantity * unit_cost) AS total_cost,
    SUM(quantity * (unit_price - unit_cost)) AS total_profit,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0),
        2
    ) AS profit_margin_pct,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales_data;

-- 4. Monthly revenue and profit
SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * unit_cost) AS cost,
    SUM(quantity * (unit_price - unit_cost)) AS profit
FROM sales_data
GROUP BY strftime('%Y-%m', order_date)
ORDER BY sales_month;

-- 5. Performance by region
SELECT
    region,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * (unit_price - unit_cost)) AS profit,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0),
        2
    ) AS profit_margin_pct
FROM sales_data
GROUP BY region
ORDER BY revenue DESC;

-- 6. Performance by product category
SELECT
    category,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * (unit_price - unit_cost)) AS profit
FROM sales_data
GROUP BY category
ORDER BY revenue DESC;

-- 7. Product profitability
SELECT
    product,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * (unit_price - unit_cost)) AS profit,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0),
        2
    ) AS profit_margin_pct
FROM sales_data
GROUP BY product
ORDER BY profit DESC;

-- 8. Customer segment comparison
SELECT
    customer_segment,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * (unit_price - unit_cost)) AS profit
FROM sales_data
GROUP BY customer_segment
ORDER BY revenue DESC;

-- 9. Basic data-quality checks
SELECT
    SUM(CASE WHEN order_id IS NULL OR TRIM(order_id) = '' THEN 1 ELSE 0 END) AS missing_order_ids,
    SUM(CASE WHEN order_date IS NULL OR date(order_date) IS NULL THEN 1 ELSE 0 END) AS invalid_dates,
    SUM(CASE WHEN quantity IS NULL OR quantity <= 0 THEN 1 ELSE 0 END) AS invalid_quantities,
    SUM(CASE WHEN unit_price IS NULL OR unit_price < 0 THEN 1 ELSE 0 END) AS invalid_prices,
    SUM(CASE WHEN unit_cost IS NULL OR unit_cost < 0 THEN 1 ELSE 0 END) AS invalid_costs
FROM sales_data;
