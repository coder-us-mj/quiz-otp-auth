from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

# Step 1: Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)

# Step 2: Custom User Model
class SignUp(AbstractUser):
    username = None  # Remove username
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    #  Use custom user manager here
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class EmailOTP(models.Model):
    email=models.EmailField()
    otp = models.CharField(max_length=6)
    created_at= models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at +timedelta(minutes = 5)
    
    def __str__(self):
        return f"{self.email} - {self.otp}"