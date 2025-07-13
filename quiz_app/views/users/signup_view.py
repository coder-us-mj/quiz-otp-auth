from rest_framework.views import APIView
from quiz_app.serializers.signup_serializer import SignupSerializer
from quiz_app.utils.otp_service import otp_service
from django.core.cache import cache
from quiz_app.common.models.user.user_otphandler import EmailOTP
from quiz_app.common.response_handler import ResponseHandler

class SignupViewSet(APIView):
    """
    Handles user signup and initiates email OTP verification.
    """
    def post(self, request):
        """
        Registers a new user and sends an OTP to their email.

        Steps:
        - Validate user input using SignupSerializer.
        - Save the user (inactive by default).
        - Generate and send OTP via email.
        - Store OTP in cache and DB for validation.
        - Return appropriate response.

        Returns:
            Response: Success or error message
        """
        try:
            serializer = SignupSerializer(data=request.data)
            
            # Validate input fields
            if serializer.is_valid():
                user = serializer.save()
                
                # Generate OTP
                otp = otp_service.generate_otp()
                
                # Cache OTP for 5 minutes
                cache.set(user.email, otp, timeout=300)
                
                # Send OTP via email
                otp_service.send_otp_email(user.email, otp)
                
                # Persist OTP in database for verification/tracking
                EmailOTP.objects.create(email=user.email, otp=otp)
                
                return ResponseHandler.handle_200_success({
                    "message": "OTP sent to your email. Verify to complete signup."
                })
            # Return serializer validation errors
            return ResponseHandler.handle_400_error(serializer.errors)
            
        except Exception as e:
            # Catch unexpected errors and return a 500 response
            return ResponseHandler.handle_500_error(request, e)