-- COP4710 G26 Project!
CREATE DATABASE BookOps;
USE BookOps;
CREATE TABLE Store
(
    store_id INT PRIMARY KEY,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(255)
);
CREATE TABLE Users
(
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);
CREATE TABLE Account
(
    account_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    store_id INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
);
CREATE TABLE Shelf
(
    shelf_id INT PRIMARY KEY,
    store_id INT NOT NULL,
    floor TINYINT NOT NULL,
    hall VARCHAR(30) NOT NULL,
    building VARCHAR(30) NOT NULL,
    FOREIGN KEY(store_id) REFERENCES Store(store_id)
);
CREATE TABLE Book
(
    book_id INT PRIMARY KEY,
    yearpublished YEAR NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    pages INT NOT NULL
);
-- end of generic code

-- Orders table to store order information
CREATE TABLE Orders
(
    order_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    order_date DATE,
    FOREIGN KEY(account_id) REFERENCES Account(account_id)
);
-- Junction table to link orders, books, and shelves
CREATE TABLE Item
(
    item_id INT PRIMARY KEY,
    order_id INT,
    shelf_id INT,
    quantity SMALLINT NOT NULL,
    book_id INT NOT NULL,
    FOREIGN KEY(order_id) REFERENCES Orders(order_id),
    FOREIGN KEY(book_id) REFERENCES Book(book_id),
    FOREIGN KEY(shelf_id) REFERENCES Shelf(shelf_id)
);

-- View: Customer-facing shelf availability
-- Shows customers what books are currently available in the store
CREATE VIEW v_available_books AS
SELECT Book.book_id,
       Book.name        AS Title,
       Book.category    AS Category,
       Book.yearpublished AS YearPublished,
       Book.pages       AS Pages,
       Book.description AS Description,
       Shelf.hall       AS Hall,
       Shelf.building   AS Building,
       Shelf.floor      AS Floor,
       Item.quantity    AS QuantityAvailable
FROM Item
JOIN Book  ON Item.book_id  = Book.book_id
JOIN Shelf ON Item.shelf_id = Shelf.shelf_id
WHERE Item.order_id IS NULL
  AND Item.quantity > 0;

-- Trigger: prevent inserting an Item with quantity less than 1
DELIMITER $$

CREATE TRIGGER trg_check_quantity
BEFORE INSERT ON Item
FOR EACH ROW
BEGIN
    IF NEW.quantity < 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantity must be at least 1';
    END IF;
END$$

DELIMITER ;
