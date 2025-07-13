from django.contrib.auth.models import AbstractUser
from django.db import models
from quiz_app.common.models.user.user_manager import CustomUserManager

class SignUp(AbstractUser):
    
    """
    Custom user model that extends Django's AbstractUser.
    Removes the default 'username' field and uses 'email' as the unique identifier for authentication.
    """
    
    # Remove the default 'username' field provided by AbstractUser    
    username = None  
    
    # Remove the default 'username' field provided by AbstractUser
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=30)

    # Use email as the field for authentication instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Attach the custom user manager that handles user creation logic
    objects = CustomUserManager()

    def __str__(self):
        """
        String representation of the user.
        Used in the admin panel and querysets.
        """
        return self.email
    
    class Meta:
        # Explicitly specify the app
        app_label = 'quiz_app'

