from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from common.response_handler import ResponseHandler


class LogoutViewSet(APIView):
    """
    Logs out an authenticated user by blacklisting their refresh token.
    Requires the user to be authenticated and provide a valid refresh token.
    """
    
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST method to blacklist the user's refresh token and invalidate their session.

        """
        try:
            # Extract refresh token from request data
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return ResponseHandler.handle_400_error("Refresh token is required.")

            # Attempt to blacklist the token (invalidates the session)
            token = RefreshToken(refresh_token)
            token.blacklist()

            return ResponseHandler.handle_200_success({
                "message": "Logged out successfully."
            })

        except TokenError:
            # Raised if the refresh token is invalid or already blacklisted
            return ResponseHandler.handle_400_error("Invalid or expired token.")

        except Exception as e:
            # Catch-all for unexpected server errors
            return ResponseHandler.handle_500_error(request, e)
