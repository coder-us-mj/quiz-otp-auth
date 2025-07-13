from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from common.response_handler import ResponseHandler



class LoginViewSet(APIView):
    """
    Handles user login using email and password authentication.
    Returns JWT access and refresh tokens upon successful authentication.
    """
    def post(self, request):
        """
        POST method to authenticate a user and return JWT tokens.

        Steps:
        - Extract email and password from request.
        - Authenticate user using Django's built-in authentication.
        - If valid and active, return JWT refresh and access tokens.
        - Handle inactive or invalid users accordingly.
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            # Authenticate using custom user model (must have AUTHENTICATION_BACKENDS set properly)
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    # Generate JWT refresh and access tokens
                    refresh = RefreshToken.for_user(user)
                    return ResponseHandler.handle_200_success({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                else:
                    return ResponseHandler.handle_400_error("Account is not activated. Verify your email OTP.")
                
            # Authentication failed (invalid credentials)
            return ResponseHandler.handle_400_error("Invalid email or password")

        except Exception as e:
            # Catch and handle unexpected server errors
            return ResponseHandler.handle_500_error(request, e)
