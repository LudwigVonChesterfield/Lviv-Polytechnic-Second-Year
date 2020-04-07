-- Q1

SELECT * FROM Employees

-- Q2

SELECT FirstName, LastName, Birthdate, Address, City, State 
FROM Employees
WHERE BirthDate = '1965-03-03 00:00:00'

-- Q3

select * from Tracks
limit 20
