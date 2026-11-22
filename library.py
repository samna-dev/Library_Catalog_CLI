# library.py
# Business logic of the library: add, search, remove, borrow and return books.
# It never prints or asks for input, that is the job of main.py.

from storage import load_catalog, save_catalog


def clean_isbn(isbn):
    """Remove spaces and dashes from an ISBN."""
    return isbn.strip().replace("-", "").replace(" ", "")


def find_book(data, isbn):
    """Return the book with this ISBN, or None if it does not exist."""
    for book in data["books"]:
        if book["isbn"] == isbn:
            return book
    return None


def add_book(isbn, title, author, copies):
    """Validate the input, add the book to the catalog and save it."""
    isbn = clean_isbn(isbn)
    title = title.strip()
    author = author.strip()

    # Input validation
    if not isbn.isdigit() or len(isbn) not in (10, 13):
        raise ValueError("ISBN must have 10 or 13 digits")
    if not title:
        raise ValueError("Title cannot be empty")
    if not author:
        raise ValueError("Author cannot be empty")
    if not isinstance(copies, int) or copies <= 0:
        raise ValueError("Copies must be a positive whole number")

    data = load_catalog()

    # Reject a duplicate ISBN
    if find_book(data, isbn) is not None:
        raise ValueError("This ISBN already exists")

    # At the start every copy is available
    new_book = {
        "isbn": isbn,
        "title": title,
        "author": author,
        "copies": copies,
        "available": copies,
    }
    data["books"].append(new_book)
    save_catalog(data)
    return new_book


def list_books():
    """Return the list of all books."""
    return load_catalog()["books"]


def search_books(query):
    """Case insensitive partial search in titles and authors."""
    query = query.strip().lower()
    if not query:
        raise ValueError("Search text cannot be empty")

    results = []
    for book in load_catalog()["books"]:
        if query in book["title"].lower() or query in book["author"].lower():
            results.append(book)
    return results


def format_book(book):
    """Return a one line text for a book."""
    return (f"{book['isbn']} | {book['title']} by {book['author']} | "
            f"{book['available']} of {book['copies']} available")


def remove_book(isbn):
    """Remove a book, but only if no copy is borrowed."""
    isbn = clean_isbn(isbn)
    data = load_catalog()

    book = find_book(data, isbn)
    if book is None:
        raise ValueError("Book not found")
    if book["available"] != book["copies"]:
        raise ValueError("Cannot remove: some copies are borrowed")

    data["books"].remove(book)
    save_catalog(data)
    return book


def borrow_book(member, isbn):
    """Lend one copy to a member and record it."""
    member = member.strip().title()
    isbn = clean_isbn(isbn)
    if not member:
        raise ValueError("Member name cannot be empty")

    data = load_catalog()
    book = find_book(data, isbn)
    if book is None:
        raise ValueError("Book not found")

    # The member must not already hold this book
    if isbn in data["members"].get(member, []):
        raise ValueError(f"{member} has already borrowed this book")

    # No book can be issued when no copy is left
    if book["available"] <= 0:
        raise ValueError("No copies available")

    book["available"] -= 1
    if member not in data["members"]:
        data["members"][member] = []
    data["members"][member].append(isbn)

    save_catalog(data)
    return book


def return_book(member, isbn):
    """Take one copy back from a member."""
    member = member.strip().title()
    isbn = clean_isbn(isbn)

    data = load_catalog()
    book = find_book(data, isbn)
    if book is None:
        raise ValueError("Book not found")

    # The member must have borrowed this book
    if isbn not in data["members"].get(member, []):
        raise ValueError(f"{member or 'This member'} did not borrow this book")

    book["available"] += 1
    data["members"][member].remove(isbn)

    # Remove the member entry when the list becomes empty
    if not data["members"][member]:
        del data["members"][member]

    save_catalog(data)
    return book