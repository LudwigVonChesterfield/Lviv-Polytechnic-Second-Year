-- Q1

SELECT COUNT(TrackId)
FROM TRACKS
WHERE Milliseconds >= 5000000

-- Q2

SELECT InvoiceID,Total
FROM Invoices
WHERE Total > 5 AND Total < 15

-- Q3

SELECT FirstName, LastName, Company, State
FROM Customers
WHERE State IN ('RJ','DF','AB','BC','CA','WA','NY')

-- Q4

SELECT CustomerId, InvoiceId, Total, InvoiceDate
FROM Invoices
WHERE CustomerID IN (56,58) AND 
Total BETWEEN 1 AND 5

-- Q5

SELECT TrackId, Name
FROM Tracks
WHERE Name LIKE 'All%'

-- Q6

SELECT CustomerId, Email
FROM Customers
WHERE Email LIKE "J%@gmail.com"

-- Q7

SELECT InvoiceId, BillingCity, Total
FROM Invoices
WHERE BillingCity IN ('Brasilia','Edmonton','Vancouver')
ORDER BY InvoiceId DESC

-- Q8

SELECT CustomerId, COUNT(*) AS Orders
FROM Invoices
GROUP BY CustomerId
ORDER BY Orders DESC

-- Q9

SELECT AlbumId, Count(*) AS Ntracks
FROM Tracks
GROUP BY AlbumId
HAVING COUNT (*) >= 12
