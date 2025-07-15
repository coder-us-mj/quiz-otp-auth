from rest_framework import serializers
from common.models.quiz.quiz_question import QuizQuestion

class QuizQuestionSerializer(serializers.ModelSerializer):
    # Include quiz title in the response for better readability (read-only)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = QuizQuestion
        fields = [
            'id', 'user', 'quiz', 'quiz_title',
            'question', 'answer_a', 'answer_b', 'answer_c', 'answer_d', 'correct_answer',
            'created_at', 'updated_at', 'deleted_at'
        ]
        read_only_fields = ['user', 'quiz','created_at', 'updated_at', 'deleted_at', 'quiz_title']
