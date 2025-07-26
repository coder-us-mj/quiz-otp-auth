from rest_framework import serializers
from common.models.quiz_attempt.quiz_attempt import QuizAttempt
from common.models.quiz.pre_quiz_answer import PreQuizAnswer
from common.models.quiz.quiz_question import QuizQuestion

# Serializer for the QuizAttempt model – used for creating, retrieving, or updating quiz attempts.
class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = '__all__'
        
# Serializer for accepting pre-quiz answers from the user – accepts question ID and answer text.
class PreQuizAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_text = serializers.CharField()

# Serializer for accepting quiz answers – includes question ID and the selected option.
class QuizAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option = serializers.CharField()
