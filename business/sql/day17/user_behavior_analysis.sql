CREATE OR REPLACE TEMP VIEW orders AS
SELECT * FROM VALUES
    (1, 101, '2026-01-05 10:00:00', 100, 'completed'),
    (2, 101, '2026-01-10 14:00:00', 200, 'completed'),
    (3, 101, '2026-01-15 09:00:00', 150, 'cancelled'),
    (4, 102, '2026-01-03 11:00:00', 300, 'completed'),
    (5, 102, '2026-01-08 16:00:00', 250, 'completed'),
    (6, 103, '2026-01-07 13:00:00', 180, 'cancelled'),
    (7, 104, '2026-01-02 09:00:00', 500, 'completed'),
    (8, 104, '2026-01-20 18:00:00', 350, 'completed')
AS orders(order_id, customer_id, order_time, amount, status);

with ranked_orders as (
    select customer_id,
           order_time,
           amount,
           row_number() over(
            partition by customer_id
            order by order_time
           ) as rn
    from orders
    where status = 'completed'
)
select customer_id,
       order_time as first_order_time,
       amount as first_order_amount
from ranked_orders
where rn = 1
;

with pre_orders as (
    select customer_id,
           order_id,
           order_time,
           lag(order_time) over(
            partition by customer_id
            order by order_time
           ) as previous_order_time
    from orders
    where status = 'completed'
)
select customer_id,
       order_id,
       order_time,
       previous_order_time,
       TIMESTAMPDIFF(DAY, previous_order_time, order_time) as days_since_previous_order
from pre_orders
;

with pre_orders as (
    select customer_id,
           order_id,
           order_time,
           amount,
           lag(order_time) over(
            partition by customer_id
            order by order_time
           ) as previous_order_time
    from orders
    where status = 'completed'
),
days_diff_orders as (
    select customer_id,
           order_id,
           order_time,
           amount,
           previous_order_time,
           TIMESTAMPDIFF(DAY, previous_order_time, order_time) as days_since_previous_order
    from pre_orders
)

select customer_id,
       count(order_id) as completed_order_count,
       coalesce(sum(amount), 0) as total_amount,
       avg(amount) as avg_order_amount,
       max(days_since_previous_order) as max_days_between_orders
from days_diff_orders
group by customer_id
;
