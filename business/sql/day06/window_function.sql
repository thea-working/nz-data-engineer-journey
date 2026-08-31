CREATE OR REPLACE TEMP VIEW user_events AS
SELECT * FROM VALUES
    (1, 'Alice', '2026-01-01 09:00:00', 'login'),
    (1, 'Alice', '2026-01-01 09:10:00', 'view'),
    (1, 'Alice', '2026-01-01 09:30:00', 'purchase'),
    (1, 'Alice', '2026-01-01 10:00:00', 'logout'),

    (2, 'Bob', '2026-01-01 09:05:00', 'login'),
    (2, 'Bob', '2026-01-01 09:20:00', 'view'),
    (2, 'Bob', '2026-01-01 09:45:00', 'logout'),

    (3, 'Cindy', '2026-01-01 10:00:00', 'login'),
    (3, 'Cindy', '2026-01-01 10:15:00', 'view')
AS user_events(user_id, name, event_time, event_type);

-- Q1: 查询每个用户的每一次行为，并显示该用户的下一次行为时间。
select user_id,
       name,
       event_time,
       event_type,
       lead(event_time, 1) over(
           partition by user_id
           order by event_time
       ) as next_event_time
from user_events
;

-- Q2: 计算每个用户当前行为到下一次行为之间相差多少分钟。
select user_id,
       name,
       event_time,
       event_type,
       next_event_time,
       timestampdiff(MINUTE,event_time,next_event_time) as minutes_to_next_event
from (
        select user_id,
               name,
               event_time,
               event_type,
               lead(event_time, 1) over(
                   partition by user_id
                   order by event_time
               ) as next_event_time
        from user_events
) user_riched_events
;
--1	Alice	2026-01-01 09:00:00	login	2026-01-01 09:10:00	10
--1	Alice	2026-01-01 09:10:00	view	2026-01-01 09:30:00	20
--1	Alice	2026-01-01 09:30:00	purchase	2026-01-01 10:00:00	30
--1	Alice	2026-01-01 10:00:00	logout	NULL	NULL
--2	Bob	2026-01-01 09:05:00	login	2026-01-01 09:20:00	15
--2	Bob	2026-01-01 09:20:00	view	2026-01-01 09:45:00	25
--2	Bob	2026-01-01 09:45:00	logout	NULL	NULL
--3	Cindy	2026-01-01 10:00:00	login	2026-01-01 10:15:00	15
--3	Cindy	2026-01-01 10:15:00	view	NULL	NULL

-- Q3: 计算每条记录所在日期的累计销售额，并观察 ROWS 和 RANGE 的区别。
CREATE OR REPLACE TEMP VIEW sales_by_day AS
SELECT * FROM VALUES
    ('2026-01-01', 100),
    ('2026-01-01', 200),
    ('2026-01-02', 300),
    ('2026-01-03', 150),
    ('2026-01-03', 250)
AS sales_by_day(sales_date, amount);

select sales_date,
       amount,
       sum(amount) over(
         order by sales_date
         range between unbounded preceding and current row
       ) as total_amount
from sales_by_day
;
--2026-01-01	100	300
--2026-01-01	200	300
--2026-01-02	300	600
--2026-01-03	150	1000
--2026-01-03	250	1000

CREATE OR REPLACE TEMP VIEW employees AS
SELECT * FROM VALUES
    (1, 'Alice', 1, 8000),
    (2, 'Bob',   1, 7000),
    (3, 'Cindy', 1, 7000),
    (4, 'David', 1, 6000),
    (5, 'Emma',  2, 9000),
    (6, 'Frank', 2, 8000),
    (7, 'Grace', 2, 8000),
    (8, 'Henry', 2, 7000),
    (9, 'Iris',  3, 9000),
    (10, 'Jack', 3, 9000),
    (11, 'Kate', 3, 7000),
    (12, 'Lucy', 3, NULL)
AS employees(employee_id, name, department_id, salary);

-- 部门表
CREATE OR REPLACE TEMP VIEW departments AS
SELECT * FROM VALUES
    (1, 'Data'),
    (2, 'HR'),
    (3, 'Engineering'),
    (4, 'Finance')
AS departments(department_id, department_name);

-- Q4: 查询每个部门的员工，并显示该部门的最高工资。
select d.department_name,
       e.name,
       e.salary,
       first_value(e.salary) over(
        partition by department_name
        order by salary desc
       ) as highest_salary
from employees e
join departments d
on e.department_id = d.department_id
;
--Data	Alice	8000	8000
--Data	Bob	7000	8000
--Data	Cindy	7000	8000
--Data	David	6000	8000
--Engineering	Iris	9000	9000
--Engineering	Jack	9000	9000
--Engineering	Kate	7000	9000
--Engineering	Lucy	NULL	9000
--HR	Emma	9000	9000
--HR	Frank	8000	9000
--HR	Grace	8000	9000
--HR	Henry	7000	9000

-- Q6: user_events 查询每个用户的所有行为，并增加两个字段：
--     该用户的第一次行为时间 first_event_time
--     当前行为与上一次行为之间的时间间隔 minutes_since_previous
select user_id,
       name,
       event_time,
       event_type,
       first_event_time,
       timestampdiff(MINUTE, previous_event_time, event_time) as minutes_since_previous
from (
        select user_id,
               name,
               event_time,
               event_type,
               first_value(event_time) over(
                    partition by user_id
                    order by event_time
               ) as first_event_time,
               lag(event_time) over(
                    partition by user_id
                    order by event_time
               ) as previous_event_time
        from user_events
) user_riched_events
;
--1	Alice	2026-01-01 09:00:00	login	2026-01-01 09:00:00	NULL
--1	Alice	2026-01-01 09:10:00	view	2026-01-01 09:00:00	10
--1	Alice	2026-01-01 09:30:00	purchase	2026-01-01 09:00:00	20
--1	Alice	2026-01-01 10:00:00	logout	2026-01-01 09:00:00	30
--2	Bob	2026-01-01 09:05:00	login	2026-01-01 09:05:00	NULL
--2	Bob	2026-01-01 09:20:00	view	2026-01-01 09:05:00	15
--2	Bob	2026-01-01 09:45:00	logout	2026-01-01 09:05:00	25
--3	Cindy	2026-01-01 10:00:00	login	2026-01-01 10:00:00	NULL
--3	Cindy	2026-01-01 10:15:00	view	2026-01-01 10:00:00	15

