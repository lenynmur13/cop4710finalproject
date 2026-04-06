-- TEST 1: Duplicate book_id (PRIMARY KEY violation)
-- Expected error:
-- ERROR 1062 (23000): Duplicate entry '1' for key 'Book.PRIMARY'
INSERT INTO Book(book_id, yearpublished, name, description, category, pages) VALUES
  (1, 2026, 'Duplicate Book', 'Trying to insert duplicate ID', 'Fiction', 100);

-- TEST 2: Invalid FK — order_id 999 does not exist
-- Expected error:
-- ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
-- (`your_db`.`Item`, CONSTRAINT `Item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `Orders` (`order_id`))
INSERT INTO Item(item_id, order_id, shelf_id, quantity, book_id) VALUES
  (8, 999, 1, 1, 2);

-- TEST 3: NULL username (NOT NULL constraint)
-- Expected error:
-- ERROR 1048 (23000): Column 'username' cannot be null
INSERT INTO Users(user_id, username, password, email) VALUES
  (5, NULL, 'nopassword', 'nulluser@example.com');
-- TEST 4: Trigger violation — quantity less than 1
-- Expected error:
-- ERROR 1644 (45000): Quantity must be at least 1
INSERT INTO Item(item_id, order_id, shelf_id, quantity, book_id) VALUES
    (99, 1, 1, 0, 1);