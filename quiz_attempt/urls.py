from django.urls import path
from quiz_attempt.views.quiz_attempt_view import access_quiz, submit_prequiz_answers, submit_quiz_answers #, view_certificate


urlpatterns = [
    path('quiz/<uuid:quiz_id>/', access_quiz, name='public-quiz-access'),
    path('quiz/<uuid:quiz_id>/pre-quiz/', submit_prequiz_answers, name='submit-prequiz'),
    path('quiz-attempt/<uuid:attempt_id>/submit/', submit_quiz_answers, name='submit-quiz'),
 #   path('quiz-attempt/<uuid:attempt_id>/certificate/', view_certificate, name='view-certificate'),
]
