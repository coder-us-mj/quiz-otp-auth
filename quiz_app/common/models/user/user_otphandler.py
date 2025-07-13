from django.db import models
from django.utils import timezone
from datetime import timedelta


class EmailOTP(models.Model):
    """
    Model to store OTPs (One-Time Passwords) sent to user emails.
    Useful for authentication flows like signup, password reset, etc.
    """
    email=models.EmailField()
    otp = models.CharField(max_length=6)
    created_at= models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """
        Checks if the OTP has expired.
        OTPs are valid for 5 minutes after creation.

        Returns:
            bool: True if OTP is expired, False otherwise.
        """
        return timezone.now() > self.created_at +timedelta(minutes = 5)
    
    def __str__(self):
        """
        String representation for admin/debugging.
        Returns the email and associated OTP.
        """
        return f"{self.email} - {self.otp}"