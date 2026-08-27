--创建学生表
CREATE OR REPLACE TEMP VIEW students AS
SELECT * FROM VALUES
    (1, 'Alice', 20, 'F'),
    (2, 'Bob',   21, 'M'),
    (3, 'Cindy', 19, 'F'),
    (4, 'David', 22, 'M'),
    (5, 'Emma',  20, 'F')
AS students(student_id, name, age, gender);

--1、查询所有不同的年龄。
select distinct age
from students
;

--20
--21
--19
--22

--2、查询年龄最大的 2 名学生。
select student_id, name, age
from students
order by age desc
limit 2
;

--4	David	22
--2	Bob	21

-- 创建员工表
CREATE OR REPLACE TEMP VIEW employees AS
SELECT * FROM VALUES
    (1, 'Alice', 'Data', 8000),
    (2, 'Bob',   'Data', NULL),
    (3, 'Cindy', 'HR',   6000),
    (4, 'David', NULL,   7500),
    (5, 'Emma',  'HR',   NULL)
AS employees(employee_id, name, department, salary);

--3、查询所有 salary 没有填写的员工。
select employee_id,
       name,
       salary
from employees
where salary is null
;

--2	Bob	NULL
--5	Emma	NULL

--4、统计员工表中实际填写了 salary 的员工数量。
select count(*) as employee_count
from employees
where salary is not null
;

--3

--5、计算所有员工的平均工资。
select round(avg(salary),2)
from employees
where salary is not null
;

--7166.666666666667

--6、统计每个 department 有多少名员工。
select department,
       count(*) as employee_count
from employees
group by department
order by department
;

--NULL	1
--Data	2
--HR	2

--7、统计每个 department 的平均工资。
select department,
       round(avg(salary),2) as avg_salary
from employees
group by department
order by avg_salary desc
;

--Data	8000.0
--NULL	7500.0
--HR	6000.0

--8、查询平均工资大于 7000 的部门。
select department,
       round(avg(salary),2) as avg_salary
from employees
group by department
having avg(salary) > 7000
;

--Data	8000.0
--NULL	7500.0

--9、查询员工人数超过 1 人的部门。
select department,
       count(*) as employee_count
from employees
group by department
having employee_count > 1
order by employee_count desc
;

--Data	2
--HR	2

--10、查询 salary 不为 NULL 的员工中，每个 department 的平均工资，只保留平均工资 ≥ 7000 的部门，并按平均工资降序排列。
select department,
       round(avg(salary),2) as avg_salary
from employees
where salary is not null
group by department
having avg(salary) >= 7000
order by avg_salary desc
;

--Data	8000.0
--NULL	7500.0

