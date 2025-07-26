# models.py

from django.db import models
from django.conf import settings
from common.models import Quiz  # Adjust this path to your actual Quiz model
from common.models.quiz.pre_quiz_question import PreQuizQuestion  # Assuming this is in the same app
import uuid

class PreQuizAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    user_email = models.EmailField(null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=255)
    
    pre_quiz_question = models.ForeignKey(PreQuizQuestion, on_delete=models.CASCADE)
    answer = models.TextField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pre_quiz_answer'
        
    def __str__(self):
        return f"{self.user.email} - {self.quiz_title} - {self.pre_quiz_question.question[:]}"
