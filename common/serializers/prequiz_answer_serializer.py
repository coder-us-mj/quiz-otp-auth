# serializers.py

from rest_framework import serializers
from common.models.quiz.pre_quiz_answer import PreQuizAnswer

class PreQuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreQuizAnswer
        fields = ['id', 'user', 'quiz', 'quiz_title', 'pre_quiz_question', 'answer', 'submitted_at']
        read_only_fields = ['user', 'submitted_at']
