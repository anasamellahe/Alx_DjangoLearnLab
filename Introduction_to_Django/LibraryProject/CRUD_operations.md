  
# This guide explains how to create Book instances using the Django interactive shell.

  

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


  

This documentation explains how to delete Book records from the database using Django's Object-Relational Mapping (ORM) module.

  

## Prerequisites

  

Before deleting records, ensure you have:

1. Started the Django shell: `python manage.py shell`

2. Imported the Book model: `from bookshelf.models import Book`

3. Existing Book records in the database to delete

  

## ⚠️ Important Warning

  

**Deletion is permanent!** Always backup your data and double-check your delete operations before executing them in production.

  

## Methods to Delete Records

  

### 1. Delete Single Record - Get and Delete

  

**Syntax:**

```python

# Step 1: Get the record

book = Book.objects.get(id=1)

  

# Step 2: Delete the record

book.delete()

```

  

**Complete Example:**

```python

try:

# Get the book to delete

book = Book.objects.get(id=1)

# Display what will be deleted

print(f"About to delete: {book.title} by {book.author} ({book.publication_year})")

# Confirm deletion

confirm = input("Are you sure? (yes/no): ")

if confirm.lower() == 'yes':

book.delete()

print("Book deleted successfully!")

else:

print("Deletion cancelled.")

except Book.DoesNotExist:

print("Book not found!")

```

  

### 2. Delete by Specific Field

  

```python

# Delete by title

try:

book = Book.objects.get(title='1984')

print(f"Deleting: {book.title}")

book.delete()

print("Book deleted!")

except Book.DoesNotExist:

print("Book with that title not found!")

  

# Delete by author and year

try:

book = Book.objects.get(author='George Orwell', publication_year=1949)

book.delete()

print("Book deleted!")

except Book.DoesNotExist:

print("Book not found!")

except Book.MultipleObjectsReturned:

print("Multiple books found! Use filter().delete() instead.")

```

  

### 3. Bulk Delete - Delete Multiple Records

  

Use `filter().delete()` to remove multiple records at once.

  

**Syntax:**

```python

Book.objects.filter(condition).delete()

```

  

**Examples:**

```python

# Delete all books by a specific author

deleted_count, details = Book.objects.filter(author='George Orwell').delete()

print(f"Deleted {deleted_count} books by George Orwell")

  

# Delete books published before 1950

deleted_count, details = Book.objects.filter(publication_year__lt=1950).delete()

print(f"Deleted {deleted_count} books published before 1950")

  

# Delete books with specific title pattern

deleted_count, details = Book.objects.filter(title__icontains='test').delete()

print(f"Deleted {deleted_count} test books")

```

  

**Understanding Delete Return Value:**

```python

result = Book.objects.filter(author='Test Author').delete()

print(result)

# Output: (2, {'bookshelf.Book': 2})

# First number: total objects deleted

# Dictionary: breakdown by model type

```

  

### 4. Delete All Records (Use with Extreme Caution!)

  

```python

# Delete ALL books (BE VERY CAREFUL!)

deleted_count, details = Book.objects.all().delete()

print(f"Deleted ALL {deleted_count} books from database!")

  

# Safer approach with confirmation

def delete_all_books():

total_books = Book.objects.count()

print(f"This will delete ALL {total_books} books!")

confirm = input("Type 'DELETE ALL' to confirm: ")

if confirm == 'DELETE ALL':

deleted_count, details = Book.objects.all().delete()

print(f"Deleted {deleted_count} books")

else:

print("Deletion cancelled")

  

# delete_all_books() # Uncomment to use

```

  

## Conditional Deletion Examples

  

### Delete by Publication Year Range

```python

# Delete books published between 1940-1950

deleted_count, details = Book.objects.filter(

publication_year__gte=1940,

publication_year__lte=1950

).delete()

print(f"Deleted {deleted_count} books from 1940-1950")

```

  

### Delete by Author Pattern

```python

# Delete all books by authors containing "Test"

deleted_count, details = Book.objects.filter(

author__icontains='test'

).delete()

print(f"Deleted {deleted_count} test books")

```

  

### Delete by Multiple Conditions

```python

# Delete specific books meeting multiple criteria

deleted_count, details = Book.objects.filter(

author='Unknown Author',

publication_year__isnull=True

).delete()

print(f"Deleted {deleted_count} books with unknown details")

```

  

## Safe Deletion Patterns

  

### 1. Preview Before Delete

```python

def safe_delete_books(author_name):

"""Safely delete books with preview and confirmation"""

# First, show what will be deleted

books_to_delete = Book.objects.filter(author=author_name)

count = books_to_delete.count()

if count == 0:

print(f"No books found by author '{author_name}'")

return

print(f"Found {count} books to delete:")

for book in books_to_delete:

print(f" - {book.title} ({book.publication_year})")

# Confirm deletion

confirm = input(f"\nDelete all {count} books? (yes/no): ")

if confirm.lower() == 'yes':

deleted_count, details = books_to_delete.delete()

print(f"Successfully deleted {deleted_count} books")

else:

print("Deletion cancelled")

  

# Usage

safe_delete_books('Test Author')

```

  

### 2. Soft Delete Alternative

```python

# Instead of deleting, mark as inactive (requires adding is_active field to model)

# Book.objects.filter(author='Old Author').update(is_active=False)

  

# To "restore" soft-deleted records:

# Book.objects.filter(author='Old Author').update(is_active=True)

```

  

## Verification After Deletion

  

### Check Single Record Deletion

```python

# Before deletion

try:

book = Book.objects.get(id=1)

print(f"Found book: {book.title}")

# Delete

book.delete()

# Verify deletion

try:

Book.objects.get(id=1)

print("ERROR: Book still exists!")

except Book.DoesNotExist:

print("Confirmed: Book deleted successfully")

except Book.DoesNotExist:

print("Book not found")

```

  

### Check Bulk Deletion Results

```python

# Count before deletion

before_count = Book.objects.filter(author='Test Author').count()

print(f"Books before deletion: {before_count}")

  

# Perform deletion

deleted_count, details = Book.objects.filter(author='Test Author').delete()

print(f"Deleted: {deleted_count}")

  

# Count after deletion

after_count = Book.objects.filter(author='Test Author').count()

print(f"Books after deletion: {after_count}")

  

# Verify

if after_count == 0:

print("✅ All books successfully deleted")

else:

print(f"⚠️ Warning: {after_count} books still remain")

```

  

## Error Handling

  

### Handle DoesNotExist Error

```python

def delete_book_by_id(book_id):

"""Delete a book by ID with proper error handling"""

try:

book = Book.objects.get(id=book_id)

title = book.title # Store title before deletion

book.delete()

print(f"Successfully deleted: {title}")

return True

except Book.DoesNotExist:

print(f"Book with ID {book_id} not found")

return False

  

# Usage

delete_book_by_id(999) # Non-existent ID

```

  

### Handle Multiple Objects with get()

```python

def delete_book_by_title(title):

"""Delete book by title with error handling"""

try:

book = Book.objects.get(title=title)

book.delete()

print(f"Deleted book: {title}")

except Book.DoesNotExist:

print(f"No book found with title: {title}")

except Book.MultipleObjectsReturned:

print(f"Multiple books found with title: {title}")

books = Book.objects.filter(title=title)

print(f"Found {books.count()} books:")

for i, book in enumerate(books, 1):

print(f" {i}. {book.title} by {book.author} ({book.publication_year})")

choice = input("Delete all? (yes/no): ")

if choice.lower() == 'yes':

deleted_count, details = books.delete()

print(f"Deleted {deleted_count} books")

  

# Usage

delete_book_by_title('Common Title')

```

  

## Advanced Deletion Patterns

  

### Delete with Related Objects (if applicable)

```python

# If your Book model had related objects, Django handles cascade deletion

# based on your model's foreign key relationships

  

# Example: If books had reviews (not in current model)

# book.delete() # Would also delete related reviews if CASCADE is set

```

  

### Conditional Deletion with Q Objects

```python

from django.db.models import Q

  

# Delete books meeting complex conditions

deleted_count, details = Book.objects.filter(

Q(publication_year__lt=1950) | Q(author__icontains='test')

).delete()

print(f"Deleted {deleted_count} books (old books or test books)")

```

  

### Batch Deletion for Large Datasets

```python

def delete_books_in_batches(filter_condition, batch_size=100):

"""Delete books in batches to avoid memory issues"""

total_deleted = 0

while True:

# Get a batch of primary keys

batch_ids = list(

Book.objects.filter(**filter_condition)

.values_list('id', flat=True)[:batch_size]

)

if not batch_ids:

break

# Delete the batch

deleted_count, details = Book.objects.filter(id__in=batch_ids).delete()

total_deleted += deleted_count

print(f"Deleted batch: {deleted_count} books")

print(f"Total deleted: {total_deleted} books")

  

# Usage for large datasets

# delete_books_in_batches({'publication_year__lt': 1900}, batch_size=50)

```

  

## Complete Deletion Example

  

```python

def deletion_examples():

"""Comprehensive deletion examples"""

print("=== Django ORM Deletion Examples ===\n")

# 1. Single record deletion

print("1. Deleting single record:")

try:

book = Book.objects.get(id=1)

print(f" Deleting: {book.title}")

book.delete()

print(" ✅ Single book deleted")

except Book.DoesNotExist:

print(" ℹ️ Book not found")

# 2. Bulk deletion

print("\n2. Bulk deletion:")

deleted_count, details = Book.objects.filter(

title__icontains='test'

).delete()

print(f" ✅ Deleted {deleted_count} test books")

# 3. Conditional deletion

print("\n3. Conditional deletion:")

deleted_count, details = Book.objects.filter(

publication_year__lt=1900

).delete()

print(f" ✅ Deleted {deleted_count} very old books")

# 4. Show remaining books

print("\n4. Remaining books:")

remaining = Book.objects.count()

print(f" 📚 {remaining} books remain in database")

  

# Run examples (uncomment to use)

# deletion_examples()

```

  

## Performance Considerations

  

### Single vs Bulk Deletion

  

| Method | Performance | Use Case | Signals Triggered |

|--------|-------------|----------|-------------------|

| `obj.delete()` | Slower | Single record, need signals | Yes |

| `queryset.delete()` | Faster | Multiple records | No |

  

### Memory Considerations

```python

# Memory-efficient for large datasets

Book.objects.filter(author='Test').delete()

  

# Memory-intensive (loads all objects first)

for book in Book.objects.filter(author='Test'):

book.delete()

```

  

## Quick Reference

  

### Deletion Methods

```python

# Single record

book = Book.objects.get(id=1)

book.delete()

  

# Multiple records

Book.objects.filter(author='Author').delete()

  

# All records (dangerous!)

Book.objects.all().delete()

```

  

### Return Values

```python

# Single delete returns: (1, {'app.Model': 1})

# Bulk delete returns: (count, {'app.Model': count})

deleted_count, model_details = queryset.delete()

```

  

## Best Practices

  

1. **Always backup data before bulk deletions**

2. **Use filter().delete() for multiple records**

3. **Preview what will be deleted first**

4. **Handle DoesNotExist exceptions**

5. **Consider soft deletion for important data**

6. **Use transactions for complex deletion operations**

7. **Test deletion logic thoroughly**

8. **Be extra careful with all().delete()**

  

## Safety Checklist

  

Before running deletion commands:

- [ ] Backup your database

- [ ] Test on development data first

- [ ] Double-check your filter conditions

- [ ] Preview what will be deleted

- [ ] Consider if soft deletion is more appropriate

- [ ] Have a recovery plan



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

print(book.title) # Output: "1984"

print(book.author) # Output: "George Orwell"

print(book.publication_year) # Output: 1949

print(book.id) # Output: 2 (auto-generated)

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

book = Book.objects.get(author='Popular Author') # May return multiple books

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


  

This documentation explains how to update Book records in the database using Django's Object-Relational Mapping (ORM) module.

  

## Prerequisites

  

Before updating records, ensure you have:

1. Started the Django shell: `python manage.py shell`

2. Imported the Book model: `from bookshelf.models import Book`

3. Existing Book records in the database to update

  

## Methods to Update Records

  

### 1. Update Single Record - Get, Modify, Save

  

This is the most common and safe method for updating individual records.

  

**Syntax:**

```python

# Step 1: Get the record

book = Book.objects.get(id=1)

  

# Step 2: Modify the fields

book.title = 'New Title'

book.author = 'New Author'

  

# Step 3: Save the changes

book.save()

```

  

**Complete Example:**

```python

try:

# Get the book to update

book = Book.objects.get(id=1)

# Display current values

print(f"Current: {book.title} by {book.author} ({book.publication_year})")

# Update the fields

book.title = 'Nineteen Eighty-Four'

book.author = 'George Orwell'

book.publication_year = 1949

# Save changes to database

book.save()

print(f"Updated: {book.title} by {book.author} ({book.publication_year})")

except Book.DoesNotExist:

print("Book not found!")

```

  

### 2. Update Multiple Records - Bulk Update

  

Use `update()` method to modify multiple records at once.

  

**Syntax:**

```python

Book.objects.filter(condition).update(field1='value1', field2='value2')

```

  

**Examples:**

```python

# Update all books by a specific author

Book.objects.filter(author='George Orwell').update(author='George Orwell (Updated)')

  

# Update publication year for books published before 1950

Book.objects.filter(publication_year__lt=1950).update(publication_year=1949)

  

# Update multiple fields for specific books

Book.objects.filter(title__icontains='gatsby').update(

title='The Great Gatsby - Classic Edition',

publication_year=1925

)

```

  

**Complete Example:**

```python

# Update all books published before 1950

updated_count = Book.objects.filter(publication_year__lt=1950).update(

publication_year=1949

)

print(f"Updated {updated_count} books")

```

  

### 3. Conditional Updates

  

Update records based on specific conditions.

  

```python

# Update books with missing publication years

Book.objects.filter(publication_year__isnull=True).update(publication_year=2023)

  

# Update books by specific author published after 1940

Book.objects.filter(

author='George Orwell',

publication_year__gt=1940

).update(author='George Orwell (Modern)')

  

# Update title case for all books

from django.db.models import F

Book.objects.all().update(title=F('title')) # This is just an example

```

  

## Update Examples by Field

  

### Update Title

```python

# Single book

book = Book.objects.get(id=1)

book.title = 'New Book Title'

book.save()

  

# Multiple books

Book.objects.filter(author='Old Author').update(title='Updated Title')

```

  

### Update Author

```python

# Single book

book = Book.objects.get(title='1984')

book.author = 'Eric Blair (George Orwell)'

book.save()

  

# Multiple books

Book.objects.filter(author='J.K. Rowling').update(author='Joanne Rowling')

```

  

### Update Publication Year

```python

# Single book

book = Book.objects.get(id=2)

book.publication_year = 2024

book.save()

  

# Multiple books

Book.objects.filter(publication_year=0).update(publication_year=2023)

```

  

## Verification After Updates

  

### Check Single Record Update

```python

# Before update

book = Book.objects.get(id=1)

print(f"Before: {book.title}")

  

# Update

book.title = 'Updated Title'

book.save()

  

# Verify update

book.refresh_from_db() # Reload from database

print(f"After: {book.title}")

```

  

### Check Bulk Update Results

```python

# Count records before update

before_count = Book.objects.filter(publication_year__lt=1950).count()

print(f"Books to update: {before_count}")

  

# Perform bulk update

updated_count = Book.objects.filter(publication_year__lt=1950).update(

publication_year=1949

)

print(f"Records updated: {updated_count}")

  

# Verify update

after_count = Book.objects.filter(publication_year=1949).count()

print(f"Books with year 1949: {after_count}")

```

  

## Advanced Update Patterns

  

### Partial Updates

```python

# Update only specific fields

book = Book.objects.get(id=1)

book.title = 'New Title'

book.save(update_fields=['title']) # Only saves the title field

```

  

### Using F() Expressions

```python

from django.db.models import F

  

# Increment publication year by 1

Book.objects.filter(id=1).update(publication_year=F('publication_year') + 1)

  

# Concatenate strings (database-level operation)

Book.objects.filter(author='George Orwell').update(

author=F('author') + ' (Classic Author)'

)

```

  

### Update with Calculations

```python

from django.db.models import Case, When, Value, CharField

  

# Conditional updates

Book.objects.update(

author=Case(

When(publication_year__lt=1950, then=Value('Classic Author')),

When(publication_year__gte=1950, then=Value('Modern Author')),

default=F('author'),

output_field=CharField()

)

)

```

  

## Error Handling

  

### Handle DoesNotExist Error

```python

try:

book = Book.objects.get(title='Nonexistent Book')

book.title = 'Updated Title'

book.save()

except Book.DoesNotExist:

print("Cannot update: Book not found!")

```

  

### Handle Multiple Objects Returned

```python

try:

book = Book.objects.get(author='Popular Author')

book.title = 'Updated Title'

book.save()

except Book.MultipleObjectsReturned:

print("Multiple books found. Use filter().update() instead:")

Book.objects.filter(author='Popular Author').update(title='Updated Title')

```

  

### Safe Update Pattern

```python

def safe_update_book(book_id, **updates):

"""Safely update a book with error handling"""

try:

book = Book.objects.get(id=book_id)

for field, value in updates.items():

if hasattr(book, field):

setattr(book, field, value)

else:

print(f"Warning: Field '{field}' doesn't exist")

book.save()

print(f"Successfully updated book: {book.title}")

return book

except Book.DoesNotExist:

print(f"Book with id {book_id} not found")

return None

  

# Usage

safe_update_book(1, title='New Title', author='New Author')

```

  

## Performance Considerations

  

### Single vs Bulk Updates

  

**Single Record Update (Slower):**

```python

# This makes individual database queries for each book

for book in Book.objects.filter(author='George Orwell'):

book.author = 'Eric Blair'

book.save() # Database query for each save

```

  

**Bulk Update (Faster):**

```python

# This makes one database query for all books

Book.objects.filter(author='George Orwell').update(author='Eric Blair')

```

  

### When to Use Each Method

  

| Method | Use When | Pros | Cons |

|--------|----------|------|------|

| `get().save()` | Single record, need validation | Triggers model methods, signals | Slower, multiple queries |

| `filter().update()` | Multiple records, simple updates | Fast, single query | No model methods/signals |

  

## Complete Update Example

  

```python

def update_book_example():

"""Complete example showing different update methods"""

print("=== Django ORM Update Examples ===\n")

# 1. Single record update

print("1. Updating single record:")

try:

book = Book.objects.get(id=1)

print(f" Before: {book.title} by {book.author}")

book.title = 'Updated: ' + book.title

book.save()

print(f" After: {book.title} by {book.author}")

except Book.DoesNotExist:

print(" Book not found!")

# 2. Bulk update

print("\n2. Bulk update:")

updated_count = Book.objects.filter(

publication_year__lt=1950

).update(author=F('author') + ' (Classic)')

print(f" Updated {updated_count} classic books")

# 3. Conditional update

print("\n3. Conditional update:")

modern_books = Book.objects.filter(publication_year__gte=2000).update(

title='Modern: ' + F('title')

)

print(f" Updated {modern_books} modern books")

  

# Run the example

# update_book_example()

```

  

## Quick Reference

  

| Method | Purpose | Database Queries | Triggers Signals |

|--------|---------|------------------|------------------|

| `obj.save()` | Update single record | 1 per save | Yes |

| `queryset.update()` | Update multiple records | 1 total | No |

| `obj.save(update_fields=[])` | Partial update | 1 per save | Yes |

| `F()` expressions | Database-level operations | 1 total | No |

  

## Best Practices

  

1. **Use `filter().update()` for bulk operations**

2. **Use `get().save()` when you need model validation**

3. **Always handle `DoesNotExist` exceptions**

4. **Use `update_fields` for partial updates**

5. **Verify updates with queries or `refresh_from_db()`**

6. **Consider using transactions for complex updates**