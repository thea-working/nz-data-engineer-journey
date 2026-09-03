CREATE OR REPLACE TEMP VIEW orders AS
SELECT * FROM VALUES
    (1, 101, '2026-01-01', 100),
    (2, 101, '2026-01-05', 200),
    (3, 101, '2026-01-10', 150),
    (4, 102, '2026-01-02', 300),
    (5, 102, '2026-01-08', 100),
    (6, 103, '2026-01-03', 500),
    (7, 103, '2026-01-15', 200),
    (8, 104, '2026-01-04', 50)
AS orders(order_id, customer_id, order_date, amount);

-- Q1: 订单总金额大于 300 的 customer
with agg_orders as (
      select customer_id,
             count(order_id) as total_orders,
             sum(amount) as total_amount
      from orders
      group by customer_id
)
select customer_id,
       total_orders,
       total_amount,
       round(total_amount / total_orders, 2) as avg_order_amount
from agg_orders
where total_amount > 300
;
--101	3	450	150.0
--102	2	400	200.0
--103	2	700	350.0

-- Q2: 找出连续两次订单之间间隔超过 5 天的客户
with order_pre as(
    select customer_id,
           order_date,
           lag(order_date) over(
            partition by customer_id
            order by order_date
           ) as previous_order_date
    from orders
),
order_diff as (
    select customer_id,
           order_date,
           previous_order_date,
           timestampdiff(DAY, previous_order_date, order_date) as days_since_previous_order
    from order_pre
)
select customer_id,
       order_date,
       previous_order_date,
       days_since_previous_order
from order_diff
where days_since_previous_order > 5
;
--102	2026-01-08	2026-01-02	6
--103	2026-01-15	2026-01-03	12

-- Q3: 找出至少有 2 笔订单的 customer，并只保留：第一次和最后一次订单之间相隔至少 7 天的 customer。
with order_top as (
    select customer_id,
           count(order_id) as total_orders,
           sum(amount) as total_amount,
           min(order_date) as first_order_date,
           max(order_date) as last_order_date
    from orders
    group by customer_id
    having count(order_id) >=2
),
customer_diff as (
    select customer_id,
           total_orders,
           total_amount,
           first_order_date,
           last_order_date,
           timestampdiff(DAY, first_order_date, last_order_date) as days_between_first_last
    from order_top
)
select customer_id,
       total_orders,
       total_amount,
       first_order_date,
       last_order_date,
       days_between_first_last
from customer_diff
where days_between_first_last >=7
;
--101	3	450	2026-01-01	2026-01-10	9
--103	2	700	2026-01-03	2026-01-15	12

