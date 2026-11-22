# main.py
# Command line menu for the Library Book Catalog.
# It only asks for input and prints results, the logic is in library.py.

from library import (add_book, remove_book, search_books, list_books,
                     borrow_book, return_book, format_book)
from storage import StorageError, load_catalog

MENU = """
===== Library Menu =====
1. View catalog
2. Search books
3. Add a book
4. Remove a book
5. Borrow a book
6. Return a book
0. Exit
"""


def show_catalog():
    books = list_books()
    if not books:
        print("The catalog is empty")
        return
    for book in books:
        print(format_book(book))


def search_menu():
    query = input("Search by title or author: ")
    try:
        results = search_books(query)
    except ValueError as e:
        print("Error:", e)
        return

    if not results:
        print("No books found")
    for book in results:
        print(format_book(book))


def add_menu():
    isbn = input("ISBN (10 or 13 digits): ")
    title = input("Title: ")
    author = input("Author: ")
    copies_text = input("Number of copies: ").strip()

    # Convert the copies to a number before calling the library
    try:
        copies = int(copies_text)
    except ValueError:
        print("Copies must be a whole number")
        return

    try:
        book = add_book(isbn, title, author, copies)
        print("Added:", book["title"])
    except ValueError as e:
        print("Error:", e)


def remove_menu():
    isbn = input("ISBN of the book to remove: ")
    try:
        book = remove_book(isbn)
        print("Removed:", book["title"])
    except ValueError as e:
        print("Error:", e)


def borrow_menu():
    member = input("Member name: ")
    isbn = input("ISBN of the book: ")
    try:
        book = borrow_book(member, isbn)
        print("Borrowed:", book["title"], "->", book["available"], "available")
    except ValueError as e:
        print("Error:", e)


def return_menu():
    member = input("Member name: ")
    isbn = input("ISBN of the book: ")
    try:
        book = return_book(member, isbn)
        print("Returned:", book["title"], "->", book["available"], "available")
    except ValueError as e:
        print("Error:", e)


# Menu number -> function (no brackets, the function is called later)
actions = {
    "1": show_catalog,
    "2": search_menu,
    "3": add_menu,
    "4": remove_menu,
    "5": borrow_menu,
    "6": return_menu,
}


def main():
    # Make sure the catalog can be read before showing the menu
    try:
        load_catalog()
    except StorageError as e:
        print("Cannot start:", e)
        return

    print("Welcome to the Library Catalog")

    # Ctrl + C or Ctrl + Z ends the program politely instead of showing an error
    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()

            if choice == "0":
                print("Goodbye!")
                break
            if choice in actions:
                try:
                    actions[choice]()
                except StorageError as e:
                    print("Storage problem:", e)
            else:
                print("Invalid option, please try again")
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()