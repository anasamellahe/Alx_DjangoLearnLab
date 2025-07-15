# Deleting Records using Django ORM

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

# delete_all_books()  # Uncomment to use
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
        print(f"  - {book.title} ({book.publication_year})")
    
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
        title = book.title  # Store title before deletion
        book.delete()
        print(f"Successfully deleted: {title}")
        return True
    except Book.DoesNotExist:
        print(f"Book with ID {book_id} not found")
        return False

# Usage
delete_book_by_id(999)  # Non-existent ID
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
            print(f"  {i}. {book.title} by {book.author} ({book.publication_year})")
        
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
# book.delete()  # Would also delete related reviews if CASCADE is set
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
        print(f"   Deleting: {book.title}")
        book.delete()
        print("   ✅ Single book deleted")
    except Book.DoesNotExist:
        print("   ℹ️ Book not found")
    
    # 2. Bulk deletion
    print("\n2. Bulk deletion:")
    deleted_count, details = Book.objects.filter(
        title__icontains='test'
    ).delete()
    print(f"   ✅ Deleted {deleted_count} test books")
    
    # 3. Conditional deletion
    print("\n3. Conditional deletion:")
    deleted_count, details = Book.objects.filter(
        publication_year__lt=1900
    ).delete()
    print(f"   ✅ Deleted {deleted_count} very old books")
    
    # 4. Show remaining books
    print("\n4. Remaining books:")
    remaining = Book.objects.count()
    print(f"   📚 {remaining} books remain in database")

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
