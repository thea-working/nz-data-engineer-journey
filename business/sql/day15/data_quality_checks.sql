CREATE OR REPLACE TEMP VIEW orders AS
SELECT * FROM VALUES
    (1, 101, '2026-01-05', 100, 'completed'),
    (2, 102, '2026-01-06', 200, 'completed'),
    (3, 103, '2026-01-07', 150, 'cancelled'),
    (4, 101, '2026-01-05', 100, 'completed'),
    (5, 104, '2026-01-08', -50, 'completed'),
    (6, 105, '2026-01-09', 300, 'pending'),
    (7, 102, '2026-01-10', 200, 'completed'),
    (8, 106, NULL, 250, 'completed'),
    (9, 107, '2026-01-12', NULL, 'completed'),
    (10, 108, '2026-01-13', 500, 'unknown')
AS orders(order_id, customer_id, order_date, amount, status);

select customer_id,
       order_date,
       amount,
       COUNT(*) AS duplicate_count
from orders
group by customer_id, order_date, amount
having count(*) > 1
;

select order_id,
       customer_id,
       amount,
       status
from orders
where amount is null
   or amount <= 0
   or order_date is null
   or status is null
   or status not in ('completed','cancelled','pending')
;

select sum(case when amount <= 0 then 1 else 0 end) as negative_or_zero_amount,
       sum(case when order_date is null then 1 else 0 end) as missing_order_date,
       sum(case when amount is null then 1 else 0 end) as missing_amount,
       sum(case when status is null or status not in ('completed','cancelled','pending') then 1 else 0 end) as invalid_status
from orders
;

