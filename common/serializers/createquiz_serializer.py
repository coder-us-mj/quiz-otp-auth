from rest_framework import serializers
from common.models.quiz.create_quiz import CreateQuiz

class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for the CreateQuiz model.
    Converts Quiz model instances to and from JSON for API interactions.
    """
    class Meta:
        model = CreateQuiz
        fields = ['id', 'title', 'created_at'] # Fields to expose in the API
        read_only_fields = ['id', 'created_at']  # Auto-managed fields, not editable by the user
