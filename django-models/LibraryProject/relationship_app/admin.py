from django.contrib import admin
from .models import Library, Librarian, Book, Author, UserProfile


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_Author_name')
    list_filter = ('author__name',)
    search_fields = ('title', 'author__name')
    def get_Author_name(self, obj):
        return obj.author.name if obj.author else 'No Library'
    get_Author_name.short_description = 'Author'


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_books_count')
    filter_horizontal = ('books',)
    
    def get_books_count(self, obj):
        return obj.books.count()
    get_books_count.short_description = 'Number of Books'


class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_library_name')
    
    def get_library_name(self, obj):
        return obj.Library.name if obj.Library else 'No Library'
    get_library_name.short_description = 'Library'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('role',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(UserProfile, UserProfileAdmin)