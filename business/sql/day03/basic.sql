-- 员工表
CREATE OR REPLACE TEMP VIEW employees AS
SELECT * FROM VALUES
    (1, 'Alice', 1, 8000),
    (2, 'Bob',   2, 7000),
    (3, 'Cindy', 1, 6000),
    (4, 'David', 3, 9000),
    (5, 'Emma',  2, NULL)
AS employees(employee_id, name, department_id, salary);

-- 部门表
CREATE OR REPLACE TEMP VIEW departments AS
SELECT * FROM VALUES
    (1, 'Data'),
    (2, 'HR'),
    (3, 'Engineering'),
    (4, 'Finance')
AS departments(department_id, department_name);

--Q1、查询所有有对应部门的员工，返回employee_id，name，department_name
select e.employee_id,
       e.name,
       d.department_name
from employees e
join departments d
on e.department_id = d.department_id
;

--1	Alice	Data
--2	Bob	HR
--3	Cindy	Data
--4	David	Engineering
--5	Emma	HR

-- Q2: 查询所有部门以及该部门的员工姓名。
select d.department_name,
       e.name
from departments d
left join employees e
on d.department_id = e.department_id
;

--Data	Cindy
--Data	Alice
--HR	Emma
--HR	Bob
--Engineering	David
--Finance	NULL

--Q3: 查询每个部门有多少名员工，包括没有员工的部门。
select department_name,
       count(employee_id) as employee_count
from (
      select d.department_name,
             e.employee_id
      from departments d
      left join employees e
      on d.department_id = e.department_id
) deEm
group by department_name
;

--Data	2
--HR	2
--Engineering	1
--Finance	0

-- 订单表
CREATE OR REPLACE TEMP VIEW orders AS
SELECT * FROM VALUES
    (101, 1, 120.50),
    (102, 1, 80.00),
    (103, 2, 300.00),
    (104, 4, 150.00),
    (105, 4, 200.00),
    (106, 4, 50.00)
AS orders(order_id, employee_id, amount);

-- Q4: 统计每位员工的订单数量。
select e.employee_id,
       e.name,
       count(o.order_id) as order_count
from employees e
left join orders o
on e.employee_id = o.employee_id
group by e.employee_id,e.name
order by order_count desc,
         e.employee_id asc
;

--4	David	3
--1	Alice	2
--2	Bob	1
--3	Cindy	0
--5	Emma	0

-- Q5: 统计每个部门的订单数量和订单总金额。
--返回department_name，order_count，total_amount，按total_amount降序排序

select d.department_name,
       count(order_id) as order_count,
       coalesce(sum(o.amount),0) as total_amount
from departments d
left join employees e
on d.department_id = e.department_id
left join orders o
on e.employee_id = o.employee_id
group by d.department_name
order by total_amount desc
;

--Engineering	3	400.00
--HR	1	300.00
--Data	2	200.50
--Finance	0	0.00

-- Q6: 查询有订单的员工姓名，以及他们的订单总金额。
-- 返回 employee_id，name，total_amount，只显示有订单的员工，按 total_amount DESC 排序
select o.employee_id,
       e.name,
       sum(o.amount) as total_amount
from orders o
join employees e
on o.employee_id = e.employee_id
group by o.employee_id,e.name
order by total_amount desc
;

--4	David	400.00
--2	Bob	300.00
--1	Alice	200.50

-- Q7: 查询每个员工的订单数量、订单总金额以及平均订单金额。
-- 所有员工都要显示, 没有订单的员工：order_count = 0, total_amount = 0, avg_amount = 0, 按 total_amount DESC 排序
select e.employee_id,
       e.name,
       count(o.order_id) as order_count,
       coalesce(sum(o.amount), 0) as total_amount,
       coalesce(avg(o.amount), 0) as avg_amount
from employees e
left join orders o
on e.employee_id = o.employee_id
group by e.employee_id, e.name
order by total_amount desc
;

--4	David	3	400.00	133.333333
--2	Bob	1	300.00	300.000000
--1	Alice	2	200.50	100.250000
--3	Cindy	0	0.00	0.000000
--5	Emma	0	0.00	0.000000
