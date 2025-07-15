from django.urls import path
from quiz_app.views.users.signup_view import SignupViewSet
from quiz_app.views.users.verifyotp_view import VerifyOTPViewSet
from quiz_app.views.users.resendotp_view import ResendOTPView
from quiz_app.views.users.login_view import LoginViewSet
from quiz_app.views.users.changepassword_view import ChangePasswordViewSet
from quiz_app.views.users.logout_view import LogoutViewSet
from quiz_app.views.quiz.quiz_view import create_quiz, get_quiz, update_quiz, delete_quiz
from quiz_app.views.quiz.quiz_question_view import add_question, update_question, get_questions, delete_question

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
    path('quiz/create/', create_quiz, name='quiz-create'),
    path('quiz/', get_quiz , name='quiz-list'),
    path('quiz/update/<uuid:quiz_id>/', update_quiz, name='quiz-update'),
    path('quiz/delete/<uuid:quiz_id>/', delete_quiz, name='quiz-delete'), 
    
    # Quiz Question Management
    path('quiz/<uuid:quiz_id>/questions/add/', add_question, name='add-question'),  # POST
    path('quiz/<uuid:quiz_id>/questions/', get_questions, name='get-questions'),    # GET
    path('quiz-question/update/<int:question_id>/', update_question, name='update-question'),  # PUT
    path('quiz-question/delete/<int:question_id>/', delete_question, name='delete-question'),  # DELETE
]
  
  