CREATE OR REPLACE TEMP VIEW customers AS
SELECT * FROM VALUES
    (101, 'Alice'),
    (102, 'Bob'),
    (103, 'Cindy'),
    (104, 'David'),
    (105, 'Emma')
AS customers(
    customer_id,
    customer_name
);

CREATE OR REPLACE TEMP VIEW customer_orders AS
SELECT * FROM VALUES
    (1, 101, '2026-01-05', 100, 'completed'),
    (2, 101, '2026-01-10', 200, 'cancelled'),

    (3, 102, '2026-01-08', 300, 'completed'),

    (4, 103, '2026-01-03', 150, 'cancelled'),
    (5, 103, '2026-01-15', 200, 'cancelled'),

    (6, 104, '2026-01-20', 500, 'completed'),

    (7, 105, '2026-01-05', 100, 'pending'),
    (8, 105, '2026-01-18', 400, 'completed')
AS customer_orders(
    order_id,
    customer_id,
    order_date,
    amount,
    status
);

select c.customer_id,
       c.customer_name
from customers c
where exists (
    select 1
    from customer_orders co
    where co.status = 'completed'
      and co.customer_id = c.customer_id
);

select c.customer_id,
       c.customer_name
from customers c
where not exists (
    select 1
    from customer_orders co
    where co.status = 'completed'
      and co.customer_id = c.customer_id
);

select c.customer_id,
       c.customer_name
from customers c
where exists (
    select 1
    from customer_orders co
    where co.status = 'completed'
      and co.customer_id = c.customer_id
) and not exists (
    select 1
    from customer_orders co
    where co.status = 'cancelled'
      and co.customer_id = c.customer_id
)
;