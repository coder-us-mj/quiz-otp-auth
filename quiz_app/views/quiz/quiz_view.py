from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from common.models.quiz.quiz import Quiz
from common.serializers.quiz_serializer import QuizSerializer
from common.response_handler import ResponseHandler  


# Create a new quiz
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quiz(request):
    """
    Create a new quiz associated with the authenticated user.
    """
    try:
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return ResponseHandler.handle_200_success({
                "message": "Quiz created successfully.",
                "quiz": serializer.data
            })
        return ResponseHandler.handle_400_error(serializer.errors)
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)


# Get all quizzes for the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz(request):
    """
    Retrieve all quizzes created by the authenticated user
    that haven't been soft-deleted.
    """
    try:
        quizzes = Quiz.objects.filter(user=request.user, deleted_at__isnull=True)
        serializer = QuizSerializer(quizzes, many=True)
        return ResponseHandler.handle_200_success(serializer.data)
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)

# Get specific quiz for the authenticated user

@api_view(['GET'])
def get_quiz_info(request, quiz_id):
    try:
        quiz = Quiz.objects.get(quiz_id=quiz_id, user=request.user, deleted_at__isnull=True)
        serializer = QuizSerializer(quiz)
        return ResponseHandler.handle_200_success(serializer.data)
    except Quiz.DoesNotExist:
        return ResponseHandler.handle_400_error('Quiz not found')


# Update an existing quiz
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_quiz(request, quiz_id):
    """
    Update a specific quiz identified by `quiz_id`,
    only if it belongs to the authenticated user and is not deleted.
    """
    try:
        quiz = Quiz.objects.get(quiz_id=quiz_id, user=request.user, deleted_at__isnull=True)
        serializer = QuizSerializer(quiz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.handle_200_success({
                "message": "Quiz updated successfully.",
                "quiz": serializer.data
            })
        return ResponseHandler.handle_400_error(serializer.errors)
    except Quiz.DoesNotExist:
        return ResponseHandler.handle_400_error('Quiz not found')
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)


# Delete a quiz 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_quiz(request, quiz_id):
    """
    delete a quiz by setting `deleted_at` timestamp.
    Only allowed if the quiz belongs to the current user.
    """
    try:
        quiz = Quiz.objects.get(quiz_id=quiz_id, user=request.user, deleted_at__isnull=True)
        quiz.deleted_at = timezone.now()
        quiz.save()
        return ResponseHandler.handle_200_success({
            "message": "Quiz deleted successfully."
        })
    except Quiz.DoesNotExist:
        return ResponseHandler.handle_400_error('Quiz not found')
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)

