-- Q1

SELECT Name,
       AlbumID
FROM Tracks
WHERE AlbumId IN (SELECT AlbumId
    FROM Albums
    WHERE Title = "Californication");
    
-- Q2

SELECT FirstName,
       LastName,
       City,
       Email,
       COUNT(I.CustomerId) AS Invoices
FROM Customers C INNER JOIN Invoices I
ON C.CustomerId = I.CustomerId
GROUP BY C.CustomerId

-- Q3

SELECT Tracks.Name,
       A.Name AS Artist,
       Albums.Title AS Album,
       Tracks.TrackId
FROM ((Tracks INNER JOIN Albums
ON Tracks.AlbumId = Albums.AlbumId)
INNER JOIN Artists A
ON A.ArtistId = Albums.ArtistId); 

-- Q4

SELECT M.LastName AS Manager, 
       E.LastName AS Employee
FROM Employees E INNER JOIN Employees M 
ON E.ReportsTo = M.EmployeeID

-- Q5

SELECT Name AS Artist,
       Artists.ArtistId,
       Albums.Title AS Album
FROM Artists
LEFT JOIN Albums
ON Artists.ArtistId = Albums.ArtistId
WHERE Album IS NULL

-- Q6

SELECT FirstName,
       LastName
FROM Employees
UNION
SELECT FirstName,
       LastName
FROM Customers
ORDER BY LastName DESC

-- Q7

SELECT C.FirstName,
       C.LastName,
       C.City AS CustomerCity,
       I.BillingCity
FROM Customers C
INNER JOIN Invoices I
ON C.CustomerId = I.CustomerId
WHERE CustomerCity != BillingCity
