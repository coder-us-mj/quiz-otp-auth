from django.urls import path
from quiz_app.views.users.signup_view import SignupViewSet
from quiz_app.views.users.verifyotp_view import VerifyOTPViewSet
from quiz_app.views.users.resendotp_view import ResendOTPView
from quiz_app.views.users.login_view import LoginViewSet
from quiz_app.views.users.changepassword_view import ChangePasswordViewSet
from quiz_app.views.quiz.createquiz_view import CreateQuizViewSet
from quiz_app.views.users.logout_view import LogoutViewSet

# URL patterns for the quiz_app's API endpoints
urlpatterns = [
    # User Authentication & Account Management
    path('signup/', SignupViewSet.as_view(), name = 'signup'),
    path('verify-otp/', VerifyOTPViewSet.as_view(), name = 'verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('change-password/', ChangePasswordViewSet.as_view(), name='change-password'),
    path('logout/', LogoutViewSet.as_view(), name='logout'),
    
    # Quiz Management
    path('create-quiz/', CreateQuizViewSet.as_view(), name='create-quiz'),  
    
]
  
  