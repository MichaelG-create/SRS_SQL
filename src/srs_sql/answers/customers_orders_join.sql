-- Total shipped amount per customer_name
SELECT
    c.customer_name,
    SUM(o.amount) AS shipped_amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'shipped'
GROUP BY c.customer_name
ORDER BY shipped_amount DESC;
