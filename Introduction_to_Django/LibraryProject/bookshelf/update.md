# Updating Records using Django ORM

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
Book.objects.all().update(title=F('title'))  # This is just an example
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
book.refresh_from_db()  # Reload from database
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
book.save(update_fields=['title'])  # Only saves the title field
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
    book.save()  # Database query for each save
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
        print(f"   Before: {book.title} by {book.author}")
        
        book.title = 'Updated: ' + book.title
        book.save()
        
        print(f"   After: {book.title} by {book.author}")
    except Book.DoesNotExist:
        print("   Book not found!")
    
    # 2. Bulk update
    print("\n2. Bulk update:")
    updated_count = Book.objects.filter(
        publication_year__lt=1950
    ).update(author=F('author') + ' (Classic)')
    
    print(f"   Updated {updated_count} classic books")
    
    # 3. Conditional update
    print("\n3. Conditional update:")
    modern_books = Book.objects.filter(publication_year__gte=2000).update(
        title='Modern: ' + F('title')
    )
    print(f"   Updated {modern_books} modern books")

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