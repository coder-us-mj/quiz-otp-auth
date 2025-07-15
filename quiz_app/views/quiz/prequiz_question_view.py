from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from common.models.quiz.pre_quiz_question import PreQuizQuestion
from common.models.quiz.quiz import Quiz
from common.serializers.prequiz_question_serializer import PreQuizQuestionSerializer
from common.response_handler import ResponseHandler


# Add a new question to a specific quiz (quiz_id passed via URL)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pre_quiz_question(request, quiz_id):
    """
    Add a question to a quiz identified by `quiz_id`.
    Only allows the authenticated user to add to their own quiz.
    """
    try:
        try:
            quiz = Quiz.objects.get(quiz_id=quiz_id, user=request.user)
        except Quiz.DoesNotExist:
            return ResponseHandler.handle_400_error("Quiz not found or does not belong to you.")

        serializer = PreQuizQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, quiz=quiz)
            return ResponseHandler.handle_200_success({
                "message": "Question added successfully.",
                "question": serializer.data
            })
        return ResponseHandler.handle_400_error(serializer.errors)
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)

# Retrieve all questions for a specific quiz
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pre_quiz_questions(request, quiz_id):
    """
    Retrieve all non-deleted questions for a quiz,
    ensuring they belong to the authenticated user.
    """
    
    try:
        questions = PreQuizQuestion.objects.filter(
            quiz__quiz_id=quiz_id,
            user=request.user,
            deleted_at__isnull=True
        )
        serializer = PreQuizQuestionSerializer(questions, many=True)
        return ResponseHandler.handle_200_success(serializer.data)
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)


# Update an existing question
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_pre_quiz_question(request, question_id):
    """
    Update a specific question (by `question_id`) only if it belongs to the current user
    and has not been soft-deleted.
    """
    
    try:
        question = PreQuizQuestion.objects.get(
            id=question_id,
            user=request.user,
            deleted_at__isnull=True
        )
        serializer = PreQuizQuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.handle_200_success({
                "message": "Question updated successfully.",
                "question": serializer.data
            })
        return ResponseHandler.handle_400_error(serializer.errors)

    except PreQuizQuestion.DoesNotExist:
        return ResponseHandler.handle_400_error("Question not found")
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)


# Delete a question (soft delete)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_pre_quiz_question(request, question_id):
    """
    Soft-delete a quiz question by setting its `deleted_at` timestamp.
    """
    try:
        question = PreQuizQuestion.objects.get(
            id=question_id,
            user=request.user,
            deleted_at__isnull=True
        )
        question.deleted_at = timezone.now()
        question.save()
        return ResponseHandler.handle_200_success({
            "message": "Question deleted."
        })

    except PreQuizQuestion.DoesNotExist:
        return ResponseHandler.handle_400_error("Question not found")
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)



















