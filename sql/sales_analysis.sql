-- Sales Performance Intelligence
-- SQL dialect: SQLite
-- Import datasets/sales_data.csv into a table named sales_data first.
-- All monetary values are in unspecified currency units.
-- Aggregation definitions match python/analyze_sales.py.

-- 1. Inspect the dataset
SELECT *
FROM sales_data
LIMIT 10;

-- 2. Dataset coverage
SELECT
    COUNT(*) AS records,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    MIN(date(order_date)) AS first_order_date,
    MAX(date(order_date)) AS last_order_date
FROM sales_data;

-- 3. Executive KPIs
SELECT
    COUNT(*) AS records,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * unit_cost) AS cost,
    SUM(quantity * (unit_price - unit_cost)) AS profit,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0), 2
    ) AS profit_margin_pct,
    ROUND(
        1.0 * SUM(quantity * unit_price) / NULLIF(COUNT(DISTINCT order_id), 0), 2
    ) AS average_order_value
FROM sales_data;

-- 4. Monthly performance (same measures as the Python summary)
SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * unit_cost) AS cost,
    SUM(quantity * (unit_price - unit_cost)) AS profit,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0), 2
    ) AS profit_margin_pct
FROM sales_data
GROUP BY strftime('%Y-%m', order_date)
ORDER BY sales_month;

-- 5. Regional performance
SELECT
    region,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * unit_cost) AS cost,
    SUM(quantity * (unit_price - unit_cost)) AS profit,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0), 2
    ) AS profit_margin_pct
FROM sales_data
GROUP BY region
ORDER BY revenue DESC, region;

-- 6. Category performance
SELECT
    category,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * unit_cost) AS cost,
    SUM(quantity * (unit_price - unit_cost)) AS profit,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0), 2
    ) AS profit_margin_pct
FROM sales_data
GROUP BY category
ORDER BY revenue DESC, category;

-- 7. Customer-segment performance
SELECT
    customer_segment,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * unit_cost) AS cost,
    SUM(quantity * (unit_price - unit_cost)) AS profit,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0), 2
    ) AS profit_margin_pct
FROM sales_data
GROUP BY customer_segment
ORDER BY revenue DESC, customer_segment;

-- 8. Product performance
SELECT
    product,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * unit_cost) AS cost,
    SUM(quantity * (unit_price - unit_cost)) AS profit,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(
        100.0 * SUM(quantity * (unit_price - unit_cost))
        / NULLIF(SUM(quantity * unit_price), 0), 2
    ) AS profit_margin_pct
FROM sales_data
GROUP BY product
ORDER BY revenue DESC, product;

-- 9. Basic data-quality checks
SELECT
    SUM(CASE WHEN order_id IS NULL OR TRIM(order_id) = '' THEN 1 ELSE 0 END) AS missing_order_ids,
    SUM(CASE WHEN order_date IS NULL OR date(order_date) IS NULL THEN 1 ELSE 0 END) AS invalid_dates,
    SUM(CASE WHEN region IS NULL OR TRIM(region) = '' THEN 1 ELSE 0 END) AS missing_regions,
    SUM(CASE WHEN sales_rep IS NULL OR TRIM(sales_rep) = '' THEN 1 ELSE 0 END) AS missing_sales_reps,
    SUM(CASE WHEN customer_segment IS NULL OR TRIM(customer_segment) = '' THEN 1 ELSE 0 END) AS missing_segments,
    SUM(CASE WHEN category IS NULL OR TRIM(category) = '' THEN 1 ELSE 0 END) AS missing_categories,
    SUM(CASE WHEN product IS NULL OR TRIM(product) = '' THEN 1 ELSE 0 END) AS missing_products,
    SUM(CASE WHEN quantity IS NULL OR quantity <= 0 THEN 1 ELSE 0 END) AS invalid_quantities,
    SUM(CASE WHEN unit_price IS NULL OR unit_price < 0 THEN 1 ELSE 0 END) AS invalid_prices,
    SUM(CASE WHEN unit_cost IS NULL OR unit_cost < 0 THEN 1 ELSE 0 END) AS invalid_costs
FROM sales_data;
