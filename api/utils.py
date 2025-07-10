import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'Your Quiz App Verification Code'
    message = f'Your Verification Code is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email]) 
    
    cache.set(email.strip(), otp, timeout=300)    