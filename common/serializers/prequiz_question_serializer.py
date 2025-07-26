from rest_framework import serializers
from common.models.quiz.pre_quiz_question import PreQuizQuestion

class PreQuizQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the PreQuizQuestion model.
    
    - Returns the ID, user, quiz reference, and question text.
    - Includes a read-only `quiz_title` field for better readability in responses.
    """
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = PreQuizQuestion
        fields = [
           'id', 'user', 'quiz', 'quiz_title',
            'question', 'created_at', 'updated_at', 'deleted_at'
        ]
        read_only_fields = ['user', 'quiz','created_at', 'updated_at', 'deleted_at', 'quiz_title']


    