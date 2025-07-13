from rest_framework import serializers

class verifyOTPSerializer(serializers.Serializer):
    """
    Serializer to verify OTP sent to user's email.
    Used in OTP-based authentication flows (e.g., signup, login, password reset).
    """
    email = serializers.EmailField() # Email address to which the OTP was sent
    otp = serializers.CharField(max_length = 6) # 6-digit OTP received by the user