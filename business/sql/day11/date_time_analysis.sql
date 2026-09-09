CREATE OR REPLACE TEMP VIEW user_orders AS
SELECT * FROM VALUES
    (1, 101, '2026-01-05', 100),
    (2, 101, '2026-01-20', 200),
    (3, 101, '2026-02-10', 150),

    (4, 102, '2026-01-15', 300),
    (5, 102, '2026-02-05', 100),
    (6, 102, '2026-02-25', 200),

    (7, 103, '2026-02-01', 500),
    (8, 103, '2026-03-10', 100),

    (9, 104, '2026-03-05', 400),
    (10, 104, '2026-03-20', 300)
AS user_orders(
    order_id,
    customer_id,
    order_date,
    amount
);

select date_trunc('month',order_date) as order_month,
       count(order_id) as total_orders,
       sum(amount) as total_amount
from user_orders
group by date_trunc('month',order_date)
order by order_month
;

with user_agg_orders as (
        select customer_id,
               min(order_date) as first_order_date,
               max(order_date) as last_order_date,
               count(order_id) as total_orders
        from user_orders
        group by customer_id
        having count(order_id) >= 2
)
select customer_id,
       first_order_date,
       last_order_date,
       total_orders,
       TIMESTAMPDIFF(DAY,first_order_date,last_order_date) as days_between_first_last
from user_agg_orders
where TIMESTAMPDIFF(DAY,first_order_date,last_order_date) >= 30
;

with customer_amount as (
    select customer_id,
           min(order_date) as first_order_date,
           count(order_id) as total_orders,
           sum(amount) as total_amount
    from user_orders
    group by customer_id
    having sum(amount) >= 300
)
select customer_id,
       date_trunc('month', first_order_date) as first_order_month,
       total_orders,
       total_amount
from customer_amount
where date_trunc('month', first_order_date) = timestamp('2026-01-01')
;
