-- Task A
\connect university

SELECT last_name, first_name FROM student 
WHERE UPPER(SUBSTRING(last_name, 1, 1)) = UPPER(SUBSTRING(first_name, 1, 1))
ORDER BY last_name, first_name;

-- Task B
\connect university

SELECT DISTINCT(SUBSTRING(UPPER(first_name), 1, 1)) AS letter, COUNT(*) AS count
FROM student
GROUP BY letter

-- Task C
\connect university

SELECT COUNT(count) AS count
FROM (SELECT COUNT(first_name) AS count
FROM student
GROUP BY first_name
HAVING count > 1) AS snt;

-- Task D
\connect university

SELECT first_name, last_name
FROM student
WHERE AGE(birth_date) > (SELECT AVG(AGE(birth_date)) FROM STUDENT);
