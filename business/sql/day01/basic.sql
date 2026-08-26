--创建学生表
CREATE OR REPLACE TEMP VIEW students AS
SELECT * FROM VALUES
    (1, 'Alice', 20, 'F'),
    (2, 'Bob',   21, 'M'),
    (3, 'Cindy', 19, 'F'),
    (4, 'David', 22, 'M'),
    (5, 'Emma',  20, 'F')
AS students(student_id, name, age, gender);

--1、查询 年龄大于 20 岁的所有学生。
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE age > 20;

--student_id  name   age  gender
------------  -----  ---  ------
--2           Bob    21   M
--4           David  22   M

--2、年龄大于等于 20 岁，并且性别为女性（F）的学生。
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE age >= 20 AND gender = 'F';

--1  Alice  20  F
--5  Emma   20  F

--3、年龄小于 21 岁，或者性别为男性（M）的学生。
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE age < 21 OR gender = 'M';

--1  Alice  20  F
--2  Bob    21  M
--3  Cindy  19  F
--4  David  22  M
--5  Emma   20  F

--4、年龄从大到小排序
SELECT student_id,
       name,
       age,
       gender
FROM students
ORDER BY age DESC;

--student_id  name   age  gender
------------  -----  ---  ------
--4           David  22   M
--2           Bob    21   M
--1           Alice  20   F
--5           Emma   20   F
--3           Cindy  19   F

--5、年龄大于等于 20 岁的学生，并按照年龄从大到小排序。
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE age >= 20
ORDER BY age DESC;

--4  David  22  M
--2  Bob    21  M
--1  Alice  20  F
--5  Emma   20  F

--6、年龄在19或22岁的学生
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE age IN (19, 22);

--3	Cindy	19	F
--4	David	22	M

--7、年龄不是 20 岁的学生。
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE age NOT IN (20);

--2	Bob	21	M
--3	Cindy	19	F
--4	David	22	M

--8、查询 年龄在 20 到 22 岁之间的所有学生。
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE age BETWEEN 20 AND 22
ORDER BY student_id
;

--1	Alice	20	F
--2	Bob	21	M
--4	David	22	M
--5	Emma	20	F

--9、现在我们要查询姓名以字母 A 开头的学生。
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE name LIKE 'A%'
ORDER BY student_id ASC
;

--1	Alice	20	F

--10、姓名中包含字母 a 的学生，但排除姓名以 A 开头的学生。
SELECT student_id,
       name,
       age,
       gender
FROM students
WHERE name LIKE '%a%' AND name NOT LIKE 'A%'
ORDER BY student_id ASC
;

--4	David	22	M
--5	Emma	20	F

