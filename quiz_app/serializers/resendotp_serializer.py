from rest_framework import serializers

class ResendOTPSerializer(serializers.Serializer):
    """
    Serializer for resending OTP to a user's email.
    Typically used when the user did not receive or the OTP expired.
    """
    email = serializers.EmailField() # Email address where the OTP should be resent