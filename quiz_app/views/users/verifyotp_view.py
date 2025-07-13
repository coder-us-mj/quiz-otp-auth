from rest_framework.views import APIView
from common.serializers.verifyotp_serializer import verifyOTPSerializer
from common.models.user.user_otphandler import EmailOTP
from common.models.user.user_signup import SignUp
from common.response_handler import ResponseHandler
from django.core.cache import cache

class VerifyOTPViewSet(APIView):
    """
    Verifies the OTP sent to the user's email.
    If valid and not expired, the user's account is activated.
    """
    def post(self, request):
        """
        Handles POST request for OTP verification.

        Steps:
        - Validate email and OTP input.
        - Check if the latest OTP exists for the provided email.
        - Validate OTP expiry and match.
        - Activate the user if OTP is valid.
        - Return appropriate success or error response.
        """
        try:
            serializer = verifyOTPSerializer(data=request.data)
            
            if serializer.is_valid():
                email = serializer.validated_data['email'].strip()
                otp_input = serializer.validated_data['otp'].strip()

                #  STEP 1: Check OTP in cache first
                cached_otp = cache.get(email)
                if not cached_otp:
                    return ResponseHandler.handle_400_error("OTP expired")

                if cached_otp != otp_input:
                    return ResponseHandler.handle_400_error("Invalid OTP")
                # Retrieve the most recent OTP entry for this email
                try:
                    otp_record = EmailOTP.objects.filter(email=email).latest('created_at')
                except EmailOTP.DoesNotExist:
                    return ResponseHandler.handle_400_error("'OTP not found. Please request again.'")

                # Check if the OTP has expired
                if otp_record.is_expired():
                    return ResponseHandler.handle_400_error("OTP expired")
                
                # Validate the OTP
                if otp_record.otp != otp_input:
                    return ResponseHandler.handle_400_error("Invalid OTP")

                # Activate user
                try:
                    user = SignUp.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    # Remove used OTP from database
                    otp_record.delete()  

                    return ResponseHandler.handle_200_success({
                        "message": "OTP verified. Account activated."
                    })
                except SignUp.DoesNotExist:
                    return ResponseHandler.handle_400_error("User not found.")
            
            # Handle input validation errors
            return ResponseHandler.handle_400_error(serializer.errors)
        
        except Exception as e:
            # Catch all unexpected e
            return ResponseHandler.handle_500_error(request, e)
