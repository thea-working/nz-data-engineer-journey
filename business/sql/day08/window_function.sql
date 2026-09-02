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

-- Q1: 查询每个员工的工资，并计算该员工工资占所在部门所有员工工资总额的百分比。
select department_name,
       name,
       salary,
       department_total,
       round(salary / department_total * 100, 2) as salary_pct
from (
    select d.department_name,
           e.name,
           e.salary,
           sum(e.salary) over (
               partition by e.department_id
           ) as department_total
    from employees e
    join departments d
      on e.department_id = d.department_id
) t;

-- Q2: 查询工资高于自己所在部门平均工资的员工。
select department_name,
       name,
       salary,
       round(avg_department_salary, 2) as avg_department_salary
from (
    select d.department_name,
           e.name,
           e.salary,
           avg(e.salary) over (
                partition by e.department_id
           ) as avg_department_salary
    from employees e
    join departments d
      on e.department_id = d.department_id
) t
where salary > avg_department_salary
;

-- Q3: 查询每个部门的员工工资排名，并计算当前员工与上一名员工之间的工资差。


select department_name,
       name,
       salary,
       salary_rank,
       previous_salary,
       salary - previous_salary as salary_difference
from (
        select d.department_name,
               e.name,
               e.salary,
               rank() over (
                    partition by e.department_id
                    order by e.salary desc
               ) as salary_rank,
               lag(e.salary) over(
                    partition by e.department_id
                    order by e.salary desc, e.employee_id
               ) as previous_salary
        from employees e
        join departments d
          on e.department_id = d.department_id
) t
;
