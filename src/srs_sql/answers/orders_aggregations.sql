-- Total amount per customer_id, ordered by total desc
SELECT
    customer_id,
    SUM(amount) AS total_amount,
    COUNT(*)    AS nb_orders
FROM orders
GROUP BY customer_id
ORDER BY total_amount DESC;
