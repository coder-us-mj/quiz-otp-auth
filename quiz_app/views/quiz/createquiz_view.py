from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from common.serializers.createquiz_serializer import QuizSerializer
from common.response_handler import ResponseHandler  


class CreateQuizViewSet(APIView):
    """
    API endpoint to create a new quiz.
    Only authenticated users can create quizzes.
    Unauthenticated users can read but not write (if GET was implemented).
    """
    
    # Allow only authenticated users to POST; others can only read (if applicable)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        """
        Handles POST request to create a new quiz.

        Steps:
        - Validate the input data using QuizSerializer.
        - Save the quiz to the database.
        - Return a success response with quiz details.
        - Handle validation and server errors gracefully.
        """
        try:
            serializer = QuizSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHandler.handle_200_success({
                    'message': 'Quiz created successfully.',
                    'quiz': serializer.data
                })
            # Return input validation errors    
            return ResponseHandler.handle_400_error(serializer.errors)

        except Exception as e:
            # Catch and handle unexpected e
            return ResponseHandler.handle_500_error(request, e)
