from
-- 员工表
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

-- Q1: 给每个部门的员工按照 salary 从高到低排名，并为每个员工生成一个行号。
select d.department_name,
       e.name,
       e.salary,
       row_number() over(
           partition by d.department_name
           order by e.salary desc
           ) as row_num
from employees e
join departments d
on e.department_id = d.department_id
;
--Data	Alice	8000	1
--Data	Bob	7000	2
--Data	Cindy	7000	3
--Data	David	6000	4
--Engineering	Iris	9000	1
--Engineering	Jack	9000	2
--Engineering	Kate	7000	3
--Engineering	Lucy	NULL	4
--HR	Emma	9000	1
--HR	Frank	8000	2
--HR	Grace	8000	3
--HR	Henry	7000	4

-- Q2: 按照每个部门内部的 salary 从高到低排名。rank()
select d.department_name,
       e.name,
       e.salary,
       rank() over(
           partition by d.department_name
           order by e.salary desc
           ) as salary_rank
from employees e
join departments d
on e.department_id = d.department_id
;
--Data	Alice	8000	1
--Data	Bob	7000	2
--Data	Cindy	7000	2
--Data	David	6000	4
--Engineering	Iris	9000	1
--Engineering	Jack	9000	1
--Engineering	Kate	7000	3
--Engineering	Lucy	NULL	4
--HR	Emma	9000	1
--HR	Frank	8000	2
--HR	Grace	8000	2
--HR	Henry	7000	4

-- Q3：查询每个部门工资最高的员工。
select department_name,
       name,
       salary
from (
      select d.department_name,
             e.name,
             e.salary,
             rank() over(
                 partition by d.department_name
                 order by e.salary desc
                 ) as salary_rank
      from employees e
      join departments d
      on e.department_id = d.department_id
) emRanked
where salary_rank = 1
;
--Data	Alice	8000
--Engineering	Iris	9000
--Engineering	Jack	9000
--HR	Emma	9000

-- Q4: 查询每个部门工资最高的 2 个员工。
select department_name,
       name,
       salary
from (
      select d.department_name,
             e.name,
             e.salary,
             rank() over(
                 partition by d.department_name
                 order by e.salary desc
                 ) as salary_rank
      from employees e
      join departments d
      on e.department_id = d.department_id
) emRanked
where salary_rank <= 2
;
--Data	Alice	8000
--Data	Bob	7000
--Data	Cindy	7000
--Engineering	Iris	9000
--Engineering	Jack	9000
--HR	Emma	9000
--HR	Frank	8000
--HR	Grace	8000

-- Q5: 查询每个部门工资最高的 2 名员工，必须严格每个部门最多返回 2 人。
select department_name,
       name,
       salary
from (
      select d.department_name,
             e.name,
             e.salary,
             row_number() over(
                 partition by d.department_name
                 order by e.salary desc, employee_id
                 ) as row_num
      from employees e
      join departments d
      on e.department_id = d.department_id
) emRanked
where row_num <= 2
;
--Data	Alice	8000
--Data	Bob	7000
--Engineering	Iris	9000
--Engineering	Jack	9000
--HR	Emma	9000
--HR	Frank	8000

CREATE OR REPLACE TEMP VIEW salary_history AS
SELECT * FROM VALUES
    (1, 'Alice', '2026-01-01', 7000),
    (1, 'Alice', '2026-02-01', 7500),
    (1, 'Alice', '2026-03-01', 8000),
    (2, 'Bob',   '2026-01-01', 6500),
    (2, 'Bob',   '2026-02-01', 7000),
    (2, 'Bob',   '2026-03-01', 6800)
AS salary_history(employee_id, name, salary_date, salary);

-- Q6: 查询每个员工每个月的工资，并显示上个月的工资。
select employee_id,
       name,
       salary_date,
       salary,
       lag(salary, 1) over(
             partition by employee_id
             order by salary_date
           ) as previous_salary
from salary_history
;
--1	Alice	2026-01-01	7000	NULL
--1	Alice	2026-02-01	7500	7000
--1	Alice	2026-03-01	8000	7500
--2	Bob	2026-01-01	6500	NULL
--2	Bob	2026-02-01	7000	6500
--2	Bob	2026-03-01	6800	7000

-- Q7: 查询每个员工每个月的工资、上个月工资，以及工资变化金额。
select employee_id,
       name,
       salary_date,
       salary,
       lag(salary, 1) over(
             partition by employee_id
             order by salary_date
           ) as previous_salary,
       salary - lag(salary, 1) over(
             partition by employee_id
             order by salary_date
           ) as salary_change
from salary_history
;

select employee_id,
       name,
       salary_date,
       salary,
       previous_salary,
       (salary - previous_salary) as salary_change
from (
      select employee_id,
             name,
             salary_date,
             salary,
             lag(salary, 1) over(
                   partition by employee_id
                   order by salary_date
                 ) as previous_salary
      from salary_history
) salPreHis
;

