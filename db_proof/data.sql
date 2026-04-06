INSERT INTO Store(store_id, phone_number, email, address) VALUES
    (1, '786-456-7890', 'storemymoney@example.com', 'SW 8th St');
INSERT INTO Users(user_id, username, password, email) VALUES
    (1, 'shiranui', 'nibiru777', 'shiranui@example.com'),
    (2, 'kazuma', 'steal123', 'kazuma@example.com'),
    (3, 'asuna', 'swordart', 'asuna@example.com');
INSERT INTO Account(account_id, user_id, store_id) VALUES
    (1, 1, 1),
    (2, 2, 1),
    (3, 3, 1);
INSERT INTO Shelf(shelf_id, store_id, floor, hall, building) VALUES
    (1, 1, 3, 'Hall A', 'Laplace'),
    (2, 1, 1, 'Hall B', 'HotelCalifornia'),
    (3, 1, 2, 'Hall C', 'Graham'),
    (4, 1, 1, 'Hall D', 'Biscayne'),
    (5, 1, 2, 'Hall E', 'PG6');
INSERT INTO Book(book_id, yearpublished, name, description, category, pages) VALUES
    (1, 2020, 'The Last Of Us', 'A novel by Joel Miller', 'Fiction', 200),
    (2, 2025, 'FastX', 'Family never surrenders', 'Superheroes', 100),
    (3, 2026, 'How to install more RAM', 'Anonymous Youtuber', 'Informational', 50),
    (4, 2015, 'Sword Art Online', 'Trapped in a VR world', 'Fantasy', 250),
    (5, 2021, 'Chainsaw Man', 'Devils and chaos', 'Horror', 180),
    (6, 2011, 'The Martian', 'Survival story on Mars', 'Sci-Fi', 369),
    (7, 2008, 'The Hunger Games', 'Fight for survival in a dystopian world', 'Fiction', 374),
    (8, 2014, 'Interstellar', 'Exploration of space and time', 'Science', 500),
    (9, 2023, 'AI Revolution', 'Impact of artificial intelligence on society', 'Technology', 290),
    (10, 2016, 'Deep Work', 'Focused success in a distracted world', 'Productivity', 296),
    (11, 2010, 'Zero to One', 'Building startups that shape the future', 'Business', 224),
    (12, 2016, 'You Don''t Know JS', 'Deep dive into JavaScript', 'Programming', 278),
    (13, 2007, 'The Kite Runner', 'Story of friendship and redemption', 'Fiction', 371),
    (14, 2019, 'Demon Slayer', 'A boy fights demons to save his sister', 'Action', 192),
    (15, 2020, 'Jujutsu Kaisen', 'Sorcerers battle cursed spirits', 'Action', 210),
    (16, 2024, 'Procrastination for Beginners', 'Why do today what you can ignore?', 'Slice of Life', 88),
    (17, 2022, 'Breaking Bad', 'Adventures of a physics teacher and his fellow student', 'Sci-Fi', 77),
    (18, 2021, '101 Ways to Annoy Your Siblings', 'Creative sibling mischief ideas', 'Humor', 120),
    (19, 2025, 'Cooking with Air: Zero Calories, Zero Effort', 'Recipes that are mostly air', 'Humor', 55),
    (20, 2023, 'The Secret Life of Socks', 'Where do all the missing socks go?', 'Humor', 99);
INSERT INTO Orders(order_id, account_id, order_date) VALUES
    (1, 1, '2026-03-04'),
    (2, 1, '2026-03-10'),
    (3, 2, '2026-03-15'),
    (4, 2, '2026-03-20');
INSERT INTO Item(item_id, order_id, shelf_id, quantity, book_id) VALUES
    (1, 1, 1, 2, 1),
    (2, 1, 3, 2, 2),
    (3, 2, 2, 1, 3),
    (4, 2, 1, 1, 1),
    (5, NULL, 4, 2, 4),
    (6, NULL, 5, 1, 5),
    (7, NULL, 4, 3, 2);

-- ── Boundary Values ───────────────────────────────────────────

-- pages = 1 (minimum meaningful page count)
INSERT INTO Book(book_id, yearpublished, name, description, category, pages) VALUES
    (21, 2024, 'The Shortest Book', 'Only one page exists', 'Humor', 1);

-- pages = 9999 (very large page count, stress test INT)
INSERT INTO Book(book_id, yearpublished, name, description, category, pages) VALUES
    (22, 2000, 'Encyclopedia of Everything', 'Covers all human knowledge', 'Reference', 9999);

-- yearpublished at minimum YEAR value MySQL accepts (1901)
INSERT INTO Book(book_id, yearpublished, name, description, category, pages) VALUES
    (23, 1901, 'The Oldest Book Here', 'Published at the boundary of MySQL YEAR type', 'History', 300);

-- quantity = 1 (minimum valid order quantity)
INSERT INTO Item(item_id, order_id, shelf_id, quantity, book_id) VALUES
    (8, 3, 2, 1, 21);

-- quantity = 32767 (max value for SMALLINT)
INSERT INTO Item(item_id, order_id, shelf_id, quantity, book_id) VALUES
    (9, 4, 3, 32767, 22);

-- floor = 0 (lowest possible floor, boundary for TINYINT)
INSERT INTO Shelf(shelf_id, store_id, floor, hall, building) VALUES
    (6, 1, 0, 'Hall F', 'Basement');

-- address = NULL (allowed in Store, tests optional field boundary)
INSERT INTO Store(store_id, phone_number, email, address) VALUES
    (2, '000-000-0000', 'nulladdress@example.com', NULL);