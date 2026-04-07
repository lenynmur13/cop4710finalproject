from functions import(
    login, register,
    get_available_books,
    get_all_books,
    get_all_orders
)

# Test login
print("── Testing login ──")
user = login("admin", "admin123")
print(user)

# Test login fail
print("\n── Testing wrong login ──")
user = login("admin", "wrongpassword")
print(user)

# Test get available books
print("\n── Testing get_available_books ──")
books = get_available_books()
for book in books:
    print(book)

# Test get all books
print("\n── Testing get_all_books ──")
books = get_all_books()
for book in books:
    print(book)

# Test get all orders
print("\n── Testing get_all_orders ──")
orders = get_all_orders()
for order in orders:
    print(order)