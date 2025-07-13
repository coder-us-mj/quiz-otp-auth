from rest_framework.views import APIView
from quiz_app.serializers.resendotp_serializer import ResendOTPSerializer
from quiz_app.common.models.user.user_otphandler import EmailOTP
from quiz_app.common.models.user.user_signup import SignUp
from quiz_app.common.response_handler import ResponseHandler
from quiz_app.utils.otp_service import otp_service
from django.core.cache import cache

# Adjust the import as needed

class ResendOTPView(APIView):
    """
    Handles resending OTP to users who haven't yet verified their accounts.
    Ensures OTP is only sent to inactive (unverified) users.
    """
    def post(self, request):
        """
        Handles POST request to resend OTP to a user's email.

        Steps:
        - Validate input email.
        - Check if the user exists.
        - If already active, return message.
        - Else generate, send, and save new OTP.
        - Return appropriate response.
        """
        try:
            serializer = ResendOTPSerializer(data=request.data)
            
            if serializer.is_valid():
                email = serializer.validated_data['email'].strip()

                try:
                    # Fetch user by email
                    user = SignUp.objects.get(email=email)

                    # If already verified, no need to send OTP
                    if user.is_active:
                        return ResponseHandler.handle_200_success({
                            "message": "User is already verified."
                        })

                    # Generate a new OTP
                    otp = otp_service.generate_otp()
                    
                    # Store in cache for 5 minutes
                    cache.set(email, otp, timeout=300)
                    
                    # Send OTP via email
                    otp_service.send_otp_email(email, otp)
                    
                    # Save OTP in the database
                    EmailOTP.objects.create(email=email, otp=otp)

                    return ResponseHandler.handle_200_success({
                        "message": "OTP resent successfully."
                    })

                except SignUp.DoesNotExist:
                    return ResponseHandler.handle_404_error()
            # Input validation failed
            return ResponseHandler.handle_400_error(serializer.errors)

        except Exception as e:
            # Catch unexpected exceptions
            return ResponseHandler.handle_500_error(request, e)
