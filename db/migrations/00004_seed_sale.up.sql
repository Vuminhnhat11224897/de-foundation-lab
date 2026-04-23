ALTER TABLE sales
ADD COLUMN IF NOT EXISTS customer_name VARCHAR(100);

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'sales'
          AND column_name = 'customer_id'
    ) THEN
        UPDATE sales s
        SET customer_name = c.customer_name
        FROM customers c
        WHERE s.customer_id = c.id
          AND s.customer_name IS NULL;

        ALTER TABLE sales DROP COLUMN customer_id CASCADE;
    END IF;
END $$;

ALTER TABLE sales DROP COLUMN IF EXISTS created_at;

DELETE FROM sales
WHERE id IN (1, 2, 3, 4, 5, 6);

INSERT INTO sales (id, customer_name, region, sale_date, amount)
VALUES
    (1, 'Alice', 'North', '2024-01-01', 500.00),
    (2, 'Bob', 'South', '2024-01-03', 600.00),
    (3, 'Alice', 'North', '2024-01-10', 700.00),
    (4, 'Charlie', 'East', '2024-01-05', 800.00),
    (5, 'Bob', 'South', '2024-01-12', 900.00),
    (6, 'Alice', 'North', '2024-01-20', 650.00);