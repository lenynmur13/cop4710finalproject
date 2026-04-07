from db import get_connection
# authentication functions. admin account is preset with username 'admin' and password 'admin123'
def login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Users WHERE username = %s AND password = %s",
        (username, password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user  # returns user dict if found, None if not

def register(username, password, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users(username, password, email, role) VALUES (%s, %s, %s, 'user')",
            (username, password, email)
        )
        user_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO Account(user_id, store_id) VALUES (%s, 1)",
            (user_id,)
        )
        conn.commit()
        return True, "Account created successfully!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# user functions

def get_available_books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM v_available_books ORDER BY Category, Title")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books

def place_order(account_id, book_id, shelf_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Orders(account_id, order_date) VALUES (%s, CURDATE())",
            (account_id,)
        )
        order_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO Item(order_id, shelf_id, quantity, book_id) VALUES (%s, %s, %s, %s)",
            (order_id, shelf_id, quantity, book_id)
        )
        conn.commit()
        return True, "Order placed successfully!"
    # trigger error handler!!!!
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def remove_order_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Item WHERE item_id = %s", (item_id,))
        conn.commit()
        return True, "Item removed successfully!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_user_orders(account_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Orders.order_id, Book.name AS BookTitle,
               Item.quantity, Orders.order_date,
               Shelf.hall, Shelf.building
        FROM Orders
        JOIN Item  ON Orders.order_id  = Item.order_id
        JOIN Book  ON Item.book_id     = Book.book_id
        JOIN Shelf ON Item.shelf_id    = Shelf.shelf_id
        WHERE Orders.account_id = %s
        ORDER BY Orders.order_date DESC
    """, (account_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders

# admin functions

def get_all_books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT book_id, name AS Title, category AS Category,
               yearpublished AS YearPublished, pages AS Pages,
               description AS Description
        FROM Book
        ORDER BY name
    """)
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books


def add_book(yearpublished, name, description, category, pages):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Book(yearpublished, name, description, category, pages)
            VALUES (%s, %s, %s, %s, %s)
        """, (yearpublished, name, description, category, pages))
        conn.commit()
        return True, "Book added successfully!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Book WHERE book_id = %s", (book_id,))
        conn.commit()
        return True, "Book deleted successfully!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Orders.order_id, Users.username AS Customer,
               Book.name AS BookTitle, Item.quantity,
               Orders.order_date, Shelf.hall, Shelf.building
        FROM Orders
        JOIN Account ON Orders.account_id = Account.account_id
        JOIN Users   ON Account.user_id   = Users.user_id
        JOIN Item    ON Orders.order_id   = Item.order_id
        JOIN Book    ON Item.book_id      = Book.book_id
        JOIN Shelf   ON Item.shelf_id     = Shelf.shelf_id
        ORDER BY Orders.order_date DESC
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders