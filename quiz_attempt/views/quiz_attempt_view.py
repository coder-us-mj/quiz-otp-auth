import uuid
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from common.response_handler import ResponseHandler 
from django.shortcuts import get_object_or_404# Adjust import as needed
from common.models.quiz_attempt.quiz_attempt import QuizAttempt
from common.models.quiz.quiz import Quiz
from common.models.quiz.quiz_question import QuizQuestion
from common.models.quiz.pre_quiz_answer import PreQuizAnswer
from common.models.quiz.pre_quiz_question import PreQuizQuestion
from common.models.quiz.certificate import CertificateTemplate, GeneratedCertificate
from common.serializers.quiz_attempt_serializer import QuizAttemptSerializer, PreQuizAnswerSerializer, QuizAnswerSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def access_quiz(request, quiz_id):
    # Fetches quiz details and its pre-quiz questions.
    try:
        quiz = Quiz.objects.get(quiz_id=quiz_id, deleted_at__isnull=True)
        pre_quiz_questions = list(quiz.prequizquestion_set.values('id', 'question'))

        return ResponseHandler.handle_200_success({
            "quiz_id": quiz.quiz_id,
            "quiz_title": quiz.title,
            "pre_quiz_questions": pre_quiz_questions
        })

    except Quiz.DoesNotExist:
        return ResponseHandler.handle_400_error('quiz not found')
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_prequiz_answers(request, quiz_id):
    # Saves pre-quiz answers and returns quiz questions for the user.
    try:
        email = request.data.get("email")
        answers = request.data.get("answers", [])

        if not email:
            return ResponseHandler.handle_400_error("Email is required.")
        if not answers:
            return ResponseHandler.handle_400_error("Answers list is required.")

        try:
            quiz = Quiz.objects.get(quiz_id=quiz_id, deleted_at__isnull=True)
        except Quiz.DoesNotExist:
            return ResponseHandler.handle_400_error("Quiz not found.")

        # Create quiz attempt
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user_email=email,
            attempt_id=uuid.uuid4()
        )

        # Validate and save each answer
        for ans in answers:
            question_id = ans.get('question_id')
            answer_text = ans.get('answer_text')

            if not question_id or not answer_text:
                return ResponseHandler.handle_400_error(
                    "Each answer must include 'question_id' and 'answer_text'."
                )

            try:
                question = PreQuizQuestion.objects.get(id=question_id)
            except PreQuizQuestion.DoesNotExist:
                return ResponseHandler.handle_400_error(
                    f"Pre-quiz question with ID {question_id} not found."
                )

            PreQuizAnswer.objects.create(
                user_email=email,
                quiz=quiz,
                quiz_title=quiz.title,
                pre_quiz_question=question,
                answer=answer_text
            )

        # Prepare quiz questions for next step
        quiz_questions = list(quiz.quizquestion_set.values(
            'id', 'question', 'answer_a', 'answer_b', 'answer_c', 'answer_d'
        ))

        return ResponseHandler.handle_200_success({
            "message": "Pre-quiz answers submitted successfully.",
            "attempt_id": str(attempt.attempt_id),
            "quiz_questions": quiz_questions
        })

    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_quiz_answers(request, attempt_id):
    # Evaluates quiz answers, calculates score, and updates attempt.
    try:
        attempt = QuizAttempt.objects.get(attempt_id=attempt_id)
        answers = request.data.get("answers", [])
        total_score = 0

        for ans in answers:
            try:
                question = QuizQuestion.objects.get(id=ans['question_id'])
                if question.correct_answer == ans['selected_option']:
                    total_score += 1
            except QuizQuestion.DoesNotExist:
                continue  # Skip invalid question IDs

        attempt.score = total_score
        attempt.completed_at = timezone.now()
        attempt.save()

        return ResponseHandler.handle_200_success({
            "message": "Quiz submitted successfully",
            "score": total_score,
            "certificate_available": True,  # Assuming certificate logic will be handled later
            "attempt_id": str(attempt.attempt_id)
        })

    except QuizAttempt.DoesNotExist:
        return ResponseHandler.handle_400_error('quiz not found')
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def view_certificate(request, certificate_id):
#     certificate = get_object_or_404(GeneratedCertificate, id=certificate_id)
#     return Response({
#         "certificate_url": request.build_absolute_uri(certificate.generated_image.url)
#     })
