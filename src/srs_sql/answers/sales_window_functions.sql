-- Running total of amount per customer ordered by sale_date
SELECT
    sale_id,
    customer_id,
    sale_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM sales
ORDER BY customer_id, sale_date;
