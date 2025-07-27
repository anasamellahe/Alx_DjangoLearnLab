# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save

# class Author(models.Model):
#     name = models.CharField(max_length=30)
#     def __str__(self):
#         return self.name

# class Book(models.Model):
#     title = models.CharField(max_length=30)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='Authors')
#     def __str__(self):
#         return self.title

# class Library(models.Model):
#     name =  models.CharField(max_length=30)
#     books = models.ManyToManyField(Book)
#     def __str__(self):
#         return self.name

# class Librarian(models.Model):
#     name =  models.CharField(max_length=30)
#     Library = models.OneToOneField(Library,  on_delete=models.CASCADE,  related_name='library')
#     def __str__(self):
#         return self.name
# # Create your models here.

# class UserProfile(models.Model):
#     user =  models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile')
#     role = models.CharField(max_length=20, choices = [('admin', 'Admin'), ('librarian','Librarian'), ('member' ,'Member')])



# def create_User_Profile(sender, instance ,created,**kwargs):
#         if created:
#             userProfile = UserProfile.objects.create(role='Admin', user=instance)
#         else:
#             print("user profile is created 2")
#             if not hasattr(instance, 'profile'):
#                 print("user profile is created 3")
#                 userProfile = UserProfile.objects.create(role='Admin', user=instance)


# post_save.connect(receiver=create_User_Profile, sender=User)



from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=30)
    books = models.ManyToManyField(Book)
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=30)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new user is registered
    """
    if created:
        UserProfile.objects.create(user=instance, role='Member')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile when User is saved (safety check)
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.get_or_create(user=instance, defaults={'role': 'Member'})