from django.db import models
from django.conf import settings
from common.models import Quiz  # Adjust the import path as needed
import uuid

class PreQuizQuestion(models.Model):
    # Reference to the quiz this question belongs to
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    # The user who created this pre-quiz question
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # The actual pre-quiz question text
    question = models.TextField()

    # Timestamps for record creation and updates
    created_at = models.DateTimeField(auto_now_add=True)  # Set only once
    updated_at = models.DateTimeField(auto_now=True)      # Updates on save
    deleted_at = models.DateTimeField(null=True, blank=True)  # For soft deletion

    class Meta:
        db_table = 'pre_quiz_question'  # Custom table name in DB

    def __str__(self):
        """
        String representation for admin and debugging.
        Shows the beginning of the question.
        """
        return f"Pre-Question: {self.question[:50]}"
