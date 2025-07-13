from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.serializers.changepassword_serializer import ChangePasswordSerializer
from common.response_handler import ResponseHandler

class ChangePasswordViewSet(APIView):
    """
    Allows an authenticated user to change their password.
    Requires current password verification before updating.
    """
    
    # Ensure the user is logged in
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST method to handle password change for authenticated users.

        Steps:
        - Validate current, new, and confirm passwords.
        - Verify the current password matches the user’s.
        - If valid, set and save the new password.
        - Return appropriate success or error response.
        """
        try:
            # Pass request context to serializer (for accessing user)
            serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                user = request.user
                
                # Set the new password (hashed automatically)
                user.set_password(serializer.validated_data['new_password'])
                user.save()

                return ResponseHandler.handle_200_success({
                    'message': 'Password changed successfully.'
                })
            # Input validation failed
            return ResponseHandler.handle_400_error(serializer.errors)

        except Exception as e:
            # Catch and handle unexpected server errors
            return ResponseHandler.handle_500_error(request, e)