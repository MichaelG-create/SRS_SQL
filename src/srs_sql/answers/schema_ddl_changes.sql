-- Create a view of active products, then select from it
CREATE OR REPLACE VIEW active_products AS
SELECT
    product_id,
    product_name,
    unit_price
FROM products
WHERE active = TRUE;

SELECT *
FROM active_products
ORDER BY product_id;
