"""
Centralized model imports for the quiz_app.
Useful for admin registration, migrations, or keeping the app interface clean.
"""
# User-related models
from quiz_app.common.models.user.user_signup import SignUp
from quiz_app.common.models.user.user_manager import CustomUserManager
from quiz_app.common.models.user.user_otphandler import EmailOTP

# Quiz-related models
from quiz_app.common.models.quiz.create_quiz import CreateQuiz