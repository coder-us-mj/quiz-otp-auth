"""
Centralized model imports for the quiz_app.
Useful for admin registration, migrations, or keeping the app interface clean.
"""
# User-related models
from common.models.user.user_signup import SignUp
from common.models.user.user_manager import CustomUserManager
from common.models.user.user_otphandler import EmailOTP

# Quiz-related models
from common.models.quiz.quiz import Quiz