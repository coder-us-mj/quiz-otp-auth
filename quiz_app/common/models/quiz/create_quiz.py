from django.db import models

class CreateQuiz(models.Model):
    """
    Model to represent a quiz entity.
    Stores the quiz title and the timestamp when it was created.
    """
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the quiz.
        Returns the quiz title for admin and shell display.
        """
        return self.title
