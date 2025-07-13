from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling user creation using email instead of username.
    This manager is used by the custom SignUp model.
    """
     
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.

        Args:
            email (str): User's email address, used as the unique identifier.
            password (str): Optional raw password for the user.
            extra_fields (dict): Additional fields like name, phone, etc.

        Raises:
            ValueError: If email is not provided.

        Returns:
            User instance
        """
        if not email:
            raise ValueError("The Email must be set")
        
        # Normalize the email (e.g., lowercase the domain part)
        email = self.normalize_email(email)
        
        # Create user instance without saving to DB yet
        user = self.model(email=email, **extra_fields)
        
        # Hash and set the password
        user.set_password(password)
        
        # Save the user to the database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with elevated permissions.

        Args:
            email (str): Email address for the superuser.
            password (str): Password for the superuser.
            extra_fields (dict): Additional fields (auto-set for admin flags).

        Returns:
            Superuser instance
        """
        
         # Ensure the superuser has admin privileges
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
 
        # Reuse the create_user logic to generate superuser
        return self.create_user(email, password, **extra_fields)