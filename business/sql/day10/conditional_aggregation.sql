CREATE OR REPLACE TEMP VIEW customer_orders AS
SELECT * FROM VALUES
    (1, 101, '2026-01-01', 100, 'completed'),
    (2, 101, '2026-01-03', 200, 'completed'),
    (3, 101, '2026-01-05', 150, 'cancelled'),
    (4, 101, '2026-01-08', 300, 'completed'),

    (5, 102, '2026-01-02', 500, 'completed'),
    (6, 102, '2026-01-06', 100, 'cancelled'),
    (7, 102, '2026-01-10', 200, 'cancelled'),

    (8, 103, '2026-01-04', 50, 'completed'),
    (9, 103, '2026-01-07', 80, 'completed'),

    (10, 104, '2026-01-05', 400, 'cancelled')
AS customer_orders(
    order_id,
    customer_id,
    order_date,
    amount,
    status
);

select customer_id,
       count(order_id) as total_orders,
       sum(case
                when status = 'completed'
                then 1
                else 0
             end
            ) as completed_orders,
       sum(case
                when status = 'cancelled'
                then 1
                else 0
             end
            ) as cancelled_orders,
       sum(case
                when status = 'completed'
                then amount
                else 0
           end
       ) as completed_amount
from customer_orders
group by customer_id
;
--101	4	3	1	600
--102	3	1	2	500
--103	2	2	0	130
--104	1	0	1	0

with agg_orders as (
    select customer_id,
           count(order_id) as total_orders,
           count(case when amount >= 200
                      then order_id
                 end
           ) as high_value_orders,
           sum(case when amount >= 200
                    then amount
                    else 0
               end
           ) as high_value_amount
    from customer_orders
    group by customer_id
)
select customer_id,
       total_orders,
       high_value_orders,
       high_value_amount,
       round(high_value_orders/total_orders * 100, 2) as high_value_order_pct
from agg_orders
;
--101	4	2	500	50.0
--102	3	2	700	66.67
--103	2	0	0	0.0
--104	1	1	400	100.0

select customer_id,
       count(order_id) as total_orders,
       sum(case
                when status = 'completed'
                then 1
                else 0
             end
            ) as completed_orders,
       sum(case
                when status = 'cancelled'
                then 1
                else 0
             end
            ) as cancelled_orders,
       sum(case
                when status = 'completed'
                then amount
                else 0
           end
       ) as completed_amount
from customer_orders
group by customer_id
having completed_amount >= 500 and cancelled_orders >= 1
;