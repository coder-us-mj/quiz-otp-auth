from django.db import models
from common.models.quiz.quiz import Quiz
from common.models.quiz.certificate import GeneratedCertificate

class QuizAttempt(models.Model):
    """
    Tracks a user's attempt on a specific quiz, including their score and certificate (if any).
    """
    attempt_id = models.UUIDField(primary_key=True, editable=False, unique=True, auto_created=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user_email = models.EmailField()  # since it's public
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    certificate = models.OneToOneField(GeneratedCertificate, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'quiz_attempt'
        
    def __str__(self):
        return f"{self.user_email} - {self.quiz.title}"
