# Creating Book Records in Django Shell

This guide explains how to create Book instances using the Django interactive shell.

## Prerequisites

Before creating Book records, ensure you have:
1. Applied migrations: `python manage.py makemigrations` and `python manage.py migrate`
2. Started the Django shell: `python manage.py shell`

## Step 1: Start Django Shell

Open your terminal in the project directory and run:
```bash
python manage.py shell
```

## Step 2: Import the Book Model

Once in the Django shell, import the Book model:
```python
from bookshelf.models import Book
```

## Step 3: Create Book Records

### Method 1: Using `objects.create()`

**Syntax:**
```python
Book.objects.create(title='title', author='author', publication_year=year)
```

**Example:**
```python
book1 = Book.objects.create(
    title='The Great Gatsby',
    author='F. Scott Fitzgerald',
    publication_year=1925
)
```

**Success Response:**
```
<Book: Book object (1)>
```

### Method 2: Using `save()`

**Example:**
```python
book2 = Book(
    title='To Kill a Mockingbird',
    author='Harper Lee',
    publication_year=1960
)
book2.save()
```

## Field Requirements

- **title**: String, maximum 200 characters
- **author**: String, maximum 100 characters  
- **publication_year**: Integer (e.g., 1925, 2023)

## Example Commands

```python
# Create multiple books
Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
Book.objects.create(title='Pride and Prejudice', author='Jane Austen', publication_year=1813)
Book.objects.create(title='The Catcher in the Rye', author='J.D. Salinger', publication_year=1951)
```

## Common Errors

### 1. Missing Required Fields
```python
# This will cause an error - missing title
Book.objects.create(author='John Doe', publication_year=2023)
```
**Error:** `IntegrityError: NOT NULL constraint failed`

### 2. String Too Long
```python
# This will cause an error - title too long (over 200 characters)
Book.objects.create(title='A' * 201, author='Author', publication_year=2023)
```
**Error:** `DataError: value too long for type`

### 3. Wrong Data Type
```python
# This will cause an error - publication_year should be integer
Book.objects.create(title='Book Title', author='Author', publication_year='not a number')
```
**Error:** `ValueError: invalid literal for int()`

## Verifying Creation

To verify your books were created successfully:

```python
# Check all books
Book.objects.all()

# Check specific book
Book.objects.get(id=1)

# Check how many books exist
Book.objects.count()
```

## Exit Django Shell

When finished, exit the shell:
```python
exit()
``` 

