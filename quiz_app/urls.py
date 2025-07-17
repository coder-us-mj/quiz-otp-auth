from django.urls import path
from quiz_app.views.users.signup_view import SignupViewSet
from quiz_app.views.users.verifyotp_view import VerifyOTPViewSet
from quiz_app.views.users.resendotp_view import ResendOTPView
from quiz_app.views.users.login_view import LoginViewSet
from quiz_app.views.users.changepassword_view import ChangePasswordViewSet
from quiz_app.views.users.logout_view import LogoutViewSet
from quiz_app.views.users.forgot_password_view import forgot_password, reset_password   
from quiz_app.views.quiz.quiz_view import create_quiz, get_quiz, update_quiz, delete_quiz
from quiz_app.views.quiz.quiz_question_view import add_question, update_question, get_questions, delete_question
from quiz_app.views.quiz.prequiz_question_view import create_pre_quiz_question, get_pre_quiz_questions, update_pre_quiz_question, delete_pre_quiz_question
from quiz_app.views.quiz.prequiz_answer_view import submit_prequiz_answer
# URL patterns for the quiz_app's API endpoints
urlpatterns = [
    
    # User Authentication & Account Management
    path('signup/', SignupViewSet.as_view(), name = 'signup'),
    path('verify-otp/', VerifyOTPViewSet.as_view(), name = 'verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('change-password/', ChangePasswordViewSet.as_view(), name='change-password'),
    path('logout/', LogoutViewSet.as_view(), name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-password/', reset_password, name='reset-password'),
    
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
    
    # PreQuiz Question Management
    path('quiz/<uuid:quiz_id>/pre-quiz-questions/add/', create_pre_quiz_question, name='create-pre-quiz-question'), #POST
    path('quiz/<uuid:quiz_id>/pre-quiz-questions/', get_pre_quiz_questions, name='get-pre-quiz-questions'),         # GET
    path('quiz/pre-quiz-questions/<int:question_id>/update/', update_pre_quiz_question, name='update-pre-quiz-question'),  # PUT
    path('quiz/pre-quiz-questions/<int:question_id>/delete/', delete_pre_quiz_question, name='delete-pre-quiz-question'),  # DELETE
    path('prequiz/answer/', submit_prequiz_answer, name='submit-prequiz-answer'),
]
  
  