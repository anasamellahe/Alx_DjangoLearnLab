# Retrieving Records from Database using Django ORM

This documentation explains how to retrieve Book records from the database using Django's Object-Relational Mapping (ORM) module.

## Prerequisites

Before retrieving records, ensure you have:
1. Started the Django shell: `python manage.py shell`
2. Imported the Book model: `from bookshelf.models import Book`
3. Created some Book records in the database

## Methods to Retrieve Records

### 1. Get a Single Record - `get()`

**Syntax:**
```python
book = Book.objects.get(field_name='value')
```

**Examples:**
```python
# Get by title
book = Book.objects.get(title='The Great Gatsby')

# Get by ID
book = Book.objects.get(id=1)

# Get by author
book = Book.objects.get(author='George Orwell')

# Get by publication year
book = Book.objects.get(publication_year=1949)
```

**Important Notes:**
- `get()` returns exactly **one** record
- Raises `DoesNotExist` error if no record found
- Raises `MultipleObjectsReturned` error if multiple records match

### 2. Get Multiple Records - `filter()`

**Examples:**
```python
# Get all books by a specific author
books = Book.objects.filter(author='J.K. Rowling')

# Get books published after 1950
books = Book.objects.filter(publication_year__gt=1950)

# Get books with title containing specific word
books = Book.objects.filter(title__icontains='gatsby')
```

### 3. Get All Records - `all()`

```python
# Get all books in the database
all_books = Book.objects.all()
```

### 4. Get First/Last Record

```python
# Get first record
first_book = Book.objects.first()

# Get last record
last_book = Book.objects.last()
```

## Accessing Record Fields

Once you have a Book record, access its fields using dot notation:

```python
book = Book.objects.get(title='1984')

# Access individual fields
print(book.title)              # Output: "1984"
print(book.author)             # Output: "George Orwell"
print(book.publication_year)   # Output: 1949
print(book.id)                 # Output: 2 (auto-generated)
```

## Complete Examples

### Example 1: Retrieve and Display Single Book
```python
try:
    book = Book.objects.get(title='The Great Gatsby')
    print(f"Title: {book.title}")
    print(f"Author: {book.author}")
    print(f"Year: {book.publication_year}")
    print(f"ID: {book.id}")
except Book.DoesNotExist:
    print("Book not found!")
```

**Expected Output:**
```
Title: The Great Gatsby
Author: F. Scott Fitzgerald
Year: 1925
ID: 1
```

### Example 2: Retrieve and Display Multiple Books
```python
books = Book.objects.filter(publication_year__gte=1950)

if books.exists():
    print("Books published after 1950:")
    for book in books:
        print(f"- {book.title} by {book.author} ({book.publication_year})")
else:
    print("No books found!")
```

## Common Query Patterns

### Field Lookups
```python
# Exact match
Book.objects.get(title__exact='1984')

# Case-insensitive match
Book.objects.filter(title__iexact='1984')

# Contains (case-sensitive)
Book.objects.filter(title__contains='Great')

# Contains (case-insensitive)
Book.objects.filter(title__icontains='great')

# Greater than
Book.objects.filter(publication_year__gt=2000)

# Less than or equal
Book.objects.filter(publication_year__lte=1950)

# In a list
Book.objects.filter(publication_year__in=[1949, 1960, 1925])
```

### Ordering Results
```python
# Order by publication year (ascending)
books = Book.objects.all().order_by('publication_year')

# Order by publication year (descending)
books = Book.objects.all().order_by('-publication_year')

# Order by multiple fields
books = Book.objects.all().order_by('author', '-publication_year')
```

## Error Handling

### Handle DoesNotExist Error
```python
try:
    book = Book.objects.get(title='Nonexistent Book')
except Book.DoesNotExist:
    print("The book does not exist in the database")
```

### Handle MultipleObjectsReturned Error
```python
try:
    book = Book.objects.get(author='Popular Author')  # May return multiple books
except Book.MultipleObjectsReturned:
    print("Multiple books found. Use filter() instead of get()")
    books = Book.objects.filter(author='Popular Author')
```

## Counting Records

```python
# Count all books
total_books = Book.objects.count()
print(f"Total books: {total_books}")

# Count filtered books
recent_books_count = Book.objects.filter(publication_year__gte=2000).count()
print(f"Books published after 2000: {recent_books_count}")
```

## Quick Reference

| Method | Purpose | Returns |
|--------|---------|---------|
| `get()` | Single record (exact match) | One object |
| `filter()` | Multiple records (conditions) | QuerySet |
| `all()` | All records | QuerySet |
| `first()` | First record | One object or None |
| `last()` | Last record | One object or None |
| `count()` | Number of records | Integer |
| `exists()` | Check if records exist | Boolean | 