from django.db import models
from django.conf import settings
from common.models.quiz.quiz import Quiz  # adjust path as needed

class QuizQuestion(models.Model):
    # Link to the user who created the question
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    question = models.TextField()
    answer_a = models.CharField(max_length=255)
    answer_b = models.CharField(max_length=255)
    answer_c = models.CharField(max_length=255)
    answer_d = models.CharField(max_length=255)
    
    # Correct answer must be one of A, B, C, or D
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
        )
    
    # Timestamps for audit and delete 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'quiz_question'
        
    def __str__(self):
        """
        Return a string representation of the question,
        showing quiz title and a preview of the question text.
        """
        return f"{self.quiz.title} - {self.question[:]}"
