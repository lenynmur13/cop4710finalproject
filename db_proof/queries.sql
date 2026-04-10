-- BookOps!!
-- COP4710 G26 Project
USE BookOps;

-- QUERY 1: List all books with their shelf location
-- Type: JOIN
SELECT Book.name AS Title, Book.category, Book.pages,
       Shelf.hall AS Hall, Shelf.building AS Building, Shelf.floor AS Floor
FROM Item
JOIN Book  ON Item.book_id  = Book.book_id
JOIN Shelf ON Item.shelf_id = Shelf.shelf_id;

-- QUERY 2: Show every shelf and what book is on it (if any)
-- Type: LEFT JOIN (shows shelves even with no items)
SELECT Shelf.shelf_id, Shelf.hall, Shelf.building, Shelf.floor,
       Book.name AS BookTitle, Book.description
FROM Shelf
LEFT JOIN Item ON Shelf.shelf_id = Item.shelf_id
LEFT JOIN Book ON Item.book_id   = Book.book_id;

-- QUERY 3: All orders with the username who placed them
-- Type: JOIN across multiple tables
SELECT Orders.order_id, Users.username, Orders.order_date
FROM Orders
JOIN Account ON Orders.account_id = Account.account_id
JOIN Users   ON Account.user_id   = Users.user_id
ORDER BY Orders.order_date;

-- QUERY 4: Total quantity of books ordered per user
-- Type: GROUP BY + aggregate (SUM)
SELECT Users.username,
       SUM(Item.quantity) AS TotalBooksordered
FROM Users
JOIN Account ON Users.user_id     = Account.user_id
JOIN Orders  ON Account.account_id = Orders.account_id
JOIN Item    ON Orders.order_id    = Item.order_id
GROUP BY Users.username;

-- QUERY 5: Books that have never been ordered (no order_id)
-- Type: WHERE with NULL check
SELECT Book.name AS Title, Book.category, Book.pages
FROM Book
JOIN Item ON Book.book_id = Item.book_id
WHERE Item.order_id IS NULL;

-- QUERY 6: Count of books per category
-- Type: GROUP BY + aggregate (COUNT)
SELECT category,
       COUNT(*) AS NumberOfBooks
FROM Book
GROUP BY category
ORDER BY NumberOfBooks DESC;

-- QUERY 7: Users who have placed more than one order
-- Type: GROUP BY + HAVING
SELECT Users.username,
       COUNT(Orders.order_id) AS TotalOrders
FROM Users
JOIN Account ON Users.user_id      = Account.user_id
JOIN Orders  ON Account.account_id = Orders.account_id
GROUP BY Users.username
HAVING COUNT(Orders.order_id) > 1;

-- QUERY 8: Find all books published after 2020
-- Type: WHERE with condition + ORDER BY
SELECT name AS Title, yearpublished, category, pages
FROM Book
WHERE yearpublished > 2020
ORDER BY yearpublished DESC;

-- QUERY 9: Full order details — user, book, shelf, quantity
-- Type: Multi-table JOIN (most complex query)
SELECT Orders.order_id    AS OrderID,
       Users.username     AS Customer,
       Book.name          AS BookTitle,
       Item.quantity      AS Quantity,
       Shelf.hall         AS Hall,
       Shelf.building     AS Building,
       Orders.order_date  AS OrderDate
FROM Orders
JOIN Account ON Orders.account_id = Account.account_id
JOIN Users   ON Account.user_id   = Users.user_id
JOIN Item    ON Orders.order_id   = Item.order_id
JOIN Book    ON Item.book_id      = Book.book_id
JOIN Shelf   ON Item.shelf_id     = Shelf.shelf_id
ORDER BY Orders.order_id;

-- QUERY 10: Books with more than 200 pages, ordered by length
-- Type: WHERE + ORDER BY
SELECT name AS Title, category, pages
FROM Book
WHERE pages > 200
ORDER BY pages DESC;

-- QUERY 11: Customer view — all available books in store
-- Type: SELECT from VIEW
SELECT * FROM v_available_books
ORDER BY Category, Title;