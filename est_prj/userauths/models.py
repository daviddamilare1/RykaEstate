from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone




# Choices

# USER_TYPE = (
#     ('Vendor', 'Vendor'),
#     ('Customer', 'Customer'),
# )


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    # Automatically fill in username if the user doan't provide any
    def save(self, *args, **kwargs):
        email_username, _ = self.email.split('@')
        if not self.username:
            self.username = email_username
        super(User, self).save(*args, **kwargs)







class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', default=None, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    # user_type = models.CharField(max_length=100, null=True, blank=True, choices=USER_TYPE ,default=None)


    def __str__(self):
        return self.user.username
    
    # Automatically fill in username if the user doan't provide any
    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

