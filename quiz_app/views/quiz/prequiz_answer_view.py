from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from common.models.quiz.pre_quiz_answer import PreQuizAnswer
from common.serializers.prequiz_answer_serializer import PreQuizAnswerSerializer
from django.shortcuts import get_object_or_404
from common.models.quiz.quiz import Quiz
from common.response_handler import ResponseHandler  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_prequiz_answer(request):
    """
    Submit a pre-quiz answer for a given quiz.
    Auto-fills quiz title and saves the answer for the authenticated user.
    """
    try:
        quiz = get_object_or_404(Quiz, id=request.data.get('quiz'))
        request.data['quiz_title'] = quiz.title  # Auto-fill title from quiz object

        serializer = PreQuizAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return ResponseHandler.handle_200_success({
                "message": "Pre-quiz answer submitted successfully.",
                "answer": serializer.data
            })

        return ResponseHandler.handle_400_error(serializer.errors)

    except Quiz.DoesNotExist:
        return ResponseHandler.handle_400_error("Quiz not found.")
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)
