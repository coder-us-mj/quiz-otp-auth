# models.py
import uuid
from django.db import models
from django.conf import settings

class Quiz(models.Model):
    """
    Model representing a quiz created by a user.
    Supports soft deletion and UUID-based identification.
    """
    quiz_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active')

    def is_active(self):
        """
        Return True if the quiz has not been soft-deleted.
        """
        return self.deleted_at is None

    def __str__(self):
        """
        String representation of the quiz object.
        """
        return self.title
