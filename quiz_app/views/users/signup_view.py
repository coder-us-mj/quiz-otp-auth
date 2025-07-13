from rest_framework.views import APIView
from common.models.user.user_signup import SignUp  # Replace with actual User model import if needed
from django.core.cache import cache
from common.serializers.signup_serializer import SignupSerializer
from common.models.user.user_otphandler import EmailOTP
from common.utils.otp_service import otp_service  # Utility service for OTP generation and sending
from common.response_handler import ResponseHandler  # Standardized response wrapper


class SignupViewSet(APIView):
    """
    Handles user signup via email and OTP verification.
    If a user with the given email already exists and is inactive, an OTP is re-sent.
    If the user does not exist, registration proceeds and OTP is sent.
    """

    def post(self, request):
        try:
            # Step 1: Check if email is provided
            email = request.data.get("email")
            if not email:
                return ResponseHandler.handle_400_error({
                    "email": ["This field is required."]
                })

            email = email.strip()

            # Step 2: Check for existing user
            existing_user = SignUp.objects.filter(email=email).first()

            if existing_user:
                if not existing_user.is_active:
                    # Case: Existing user, but not verified — resend OTP
                    otp = otp_service.generate_otp()
                    cache.set(email, otp, timeout=300)
                    otp_service.send_otp_email(email, otp)

                    # Update or create OTP entry in database
                    EmailOTP.objects.update_or_create(
                        email=email,
                        defaults={"otp": otp}
                    )

                    return ResponseHandler.handle_200_success({
                        "message": "OTP re-sent to your email. Verify to complete signup."
                    })

                # Case: User already verified
                return ResponseHandler.handle_400_error({
                    "email": ["This email is already registered and verified."]
                })

            # Step 3: New user registration flow
            serializer = SignupSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()

                # Generate and send OTP for email verification
                otp = otp_service.generate_otp()
                cache.set(user.email, otp, timeout=300)
                otp_service.send_otp_email(user.email, otp)

                # Save OTP in database for reference/verification
                EmailOTP.objects.create(email=user.email, otp=otp)

                return ResponseHandler.handle_200_success({
                    "message": "OTP sent to your email. Verify to complete signup."
                })

            # Validation failed
            return ResponseHandler.handle_400_error(serializer.errors)

        except Exception as e:
            # Catch and return internal server errors
            return ResponseHandler.handle_500_error(request, e)
