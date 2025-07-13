import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

class otp_service:
    """
    Service class for handling OTP generation and delivery.
    Handles sending OTP via email and caching it temporarily for verification.
    """

    @staticmethod
    def generate_otp():
      """
        Generates a 6-digit numeric OTP as a string.

        Returns:
            str: A randomly generated 6-digit OTP
        """
      return str(random.randint(100000, 999999))
    @staticmethod
    def send_otp_email(email, otp):
      """
        Sends the OTP to the user's email and caches it for 5 minutes.

        Args:
            email (str): Recipient's email address
            otp (str): The OTP to be sent

        Side Effects:
            - Sends an email using Django's email backend
            - Stores the OTP in cache with a 5-minute expiration
        """
      subject = 'Your Quiz App Verification Code'
      message = f'Your Verification Code is: {otp}'
      
      # Send OTP email
      send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
      
      # Store OTP in cache with 5-minute expiration (300 seconds) 
      cache.set(email.strip(), otp, timeout=300)    