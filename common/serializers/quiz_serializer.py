from rest_framework import serializers
from common.models.quiz.quiz import Quiz

class QuizSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    """
    Serializer for the Quiz model.
    Handles serialization and deserialization of Quiz instances,
    and includes dynamic status handling (active/deleted).
    """
    class Meta:
        model = Quiz
        fields = ['quiz_id', 'title', 'description', 'status']

    def get_status(self, obj):
        """
        Dynamically return the status of the quiz:
        """
        return "active" if obj.deleted_at is None else "deleted"
