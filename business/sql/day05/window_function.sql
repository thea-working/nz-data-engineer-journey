-- 创建销售数据表
CREATE OR REPLACE TEMP VIEW daily_sales AS
SELECT * FROM VALUES
    ('2026-01-01', 1000),
    ('2026-01-02', 1500),
    ('2026-01-03', 800),
    ('2026-01-04', 1200),
    ('2026-01-05', 1800)
AS daily_sales(sales_date, amount);

-- Q1: 计算每天的销售额，以及截至当天为止的累计销售额。
select sales_date,
       amount,
       sum(amount) over(
            order by sales_date
            rows between unbounded preceding and current row
       ) as running_total
from daily_sales
;
--2026-01-01	1000	1000
--2026-01-02	1500	2500
--2026-01-03	800	    3300
--2026-01-04	1200	4500
--2026-01-05	1800	6300

-- Q2: 计算每天的销售额，以及当天和前两天的 3-day moving average。
select sales_date,
       amount,
       round(
             avg(amount) over(
                order by sales_date
                rows between 2 preceding and current row
       ), 2) as 3_day_avg
from daily_sales
;
--2026-01-01	1000	1000.0
--2026-01-02	1500	1250.0
--2026-01-03	800	1100.0
--2026-01-04	1200	1166.67
--2026-01-05	1800	1266.67

-- Q3: 计算每天的销售额，以及相比前一天销售额的变化金额和变化百分比。
select sales_date,
       amount,
       previous_amount,
       amount - previous_amount as amount_change,
       case
         when previous_amount is not null and previous_amount != 0
         then round((amount - previous_amount) / previous_amount * 100,2)
         else null
       end as change_pct
from (
      select sales_date,
             amount,
             lag(amount, 1) over(
                 order by sales_date
                ) as previous_amount
      from daily_sales
) daily_sales_rich
;
--2026-01-01	1000	NULL	NULL	NULL
--2026-01-02	1500	1000	500	50.0
--2026-01-03	800	1500	-700	-46.67
--2026-01-04	1200	800	400	50.0
--2026-01-05	1800	1200	600	50.0

-- Q4: 计算每个产品每天的销售额，以及该产品截至当天的累计销售额。
CREATE OR REPLACE TEMP VIEW product_sales AS
SELECT * FROM VALUES
    ('2026-01-01', 'A', 100),
    ('2026-01-02', 'A', 150),
    ('2026-01-03', 'A', 120),
    ('2026-01-01', 'B', 200),
    ('2026-01-02', 'B', 180),
    ('2026-01-03', 'B', 220)
AS product_sales(sales_date, product, amount);

select product,
       sales_date,
       amount,
       sum(amount) over(
           partition by product
           order by sales_date
           rows between unbounded preceding and current row
       ) as sum_amount
from product_sales
;
--A	2026-01-01	100	100
--A	2026-01-02	150	250
--A	2026-01-03	120	370
--B	2026-01-01	200	200
--B	2026-01-02	180	380
--B	2026-01-03	220	600