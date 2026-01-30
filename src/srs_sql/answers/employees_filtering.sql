-- Employees in Engineering hired after 2020-01-01, ordered by salary desc
SELECT
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    hire_date
FROM employees
WHERE department = 'Engineering'
  AND CAST(hire_date AS DATE) > DATE '2020-01-01'
ORDER BY salary DESC;
