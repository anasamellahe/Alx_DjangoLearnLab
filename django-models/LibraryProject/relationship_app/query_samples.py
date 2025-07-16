# This script should contain the query for each of the following of relationship:
# Query all books by a specific author.
# List all books in a library.
# Retrieve the librarian for a library.

from .models import Book, Author, Librarian, Library

# Query all books by a specific author.
print("=== Query all books by a specific author ===")
books_by_author = Book.objects.filter(author__name=author_name)
for book in books_by_author:
    print(f"Book: {book.title}")

print("\n=== List all books in a library ===")
# List all books in a library.
library_instance = Library.objects.get(name=library_name)
books_in_library = library_instance.books.all()

for book in books_in_library:
    print(f"Book in library: {book.title}")

print("\n=== Retrieve the librarian for a library ===")
# Retrieve the librarian for a library.
library_for_librarian = Library.objects.get(name=library_name)
librarian_for_library = library_for_librarian.library  # Using related_name to get the librarian object
print(f"Librarian for {library_for_librarian.name}: {librarian_for_library.name}")
