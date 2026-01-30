-- Multi-step ETL-style query with CTEs
WITH daily AS (
    SELECT
        sale_date,
        SUM(amount) AS total_amount
    FROM sales
    GROUP BY sale_date
),
stats AS (
    SELECT
        AVG(total_amount) AS avg_amount
    FROM daily
),
above_avg AS (
    SELECT
        d.sale_date,
        d.total_amount,
        CASE
            WHEN d.total_amount > s.avg_amount THEN 'above_average'
            ELSE 'below_or_equal_average'
        END AS sales_level
    FROM daily d
    CROSS JOIN stats s
)
SELECT
    sale_date,
    total_amount,
    sales_level
FROM above_avg
ORDER BY sale_date;
