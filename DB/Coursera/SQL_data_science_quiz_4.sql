-- Q1

SELECT CustomerId,
       FirstName || " " || LastName AS FullName,
       Address,
       UPPER(City || " " || Country) AS CityCountry
FROM Customers

-- Q2

SELECT FirstName,
       LastName,
       LOWER(SUBSTR(FirstName,1,4)) AS A,
       LOWER(SUBSTR(LastName,1,2)) AS B,
       LOWER(SUBSTR(FirstName,1,4)) || LOWER(SUBSTR(LastName,1,2)) AS userId
FROM Employees

-- Q3

SELECT FirstName,
       LastName,
       HireDate,
       (STRFTIME('%Y', 'now') - STRFTIME('%Y', HireDate)) 
          - (STRFTIME('%m-%d', 'now') < STRFTIME('%m-%d', HireDate)) 
          AS YearsWorked
FROM Employees
WHERE YearsWorked >= 15
ORDER BY LastName ASC

-- Q4

SELECT COUNT(*)
FROM Customers
WHERE [some_column] IS NULL

-- Q5

SELECT City,
       COUNT(*)
FROM Customers
GROUP BY City
ORDER BY COUNT(*) DESC

-- Q6

SELECT C.FirstName,
       C.LastName,
       I.InvoiceId,
       C.FirstName || C.LastName || I.InvoiceID AS NewId
FROM Customers C INNER JOIN Invoices I
ON C.CustomerId = I.CustomerID
WHERE NewId LIKE 'AstridGruber%'
