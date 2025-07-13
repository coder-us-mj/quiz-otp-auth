from rest_framework import serializers
from common.models.user.user_signup import SignUp
from django.contrib.auth.password_validation import validate_password

class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.
    Handles user input validation, password confirmation, and user creation logic.
    """
    confirm_password = serializers.CharField(write_only=True) # Field to confirm password input

    class Meta:
        model = SignUp
        fields = ['name', 'email', 'designation', 'phone', 'district', 'state', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}} # Hide password in API responses

    def validate(self, data):
        """
        Validates that passwords match and meet strength requirements.

        Args:
            data (dict): Input data from user

        Raises:
            ValidationError: If passwords do not match or are weak

        Returns:
            dict: Validated data
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['password'])  # Django's built-in validator
        return data

    def create(self, validated_data):
        """
        Creates a new user after validating input data.

        Args:
            validated_data (dict): Sanitized data from validated() method

        Returns:
            SignUp instance
        """
        # Remove confirm_password as it's not part of the user model
        validated_data.pop('confirm_password')
        # Create user using custom manager method
        user = SignUp.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            designation=validated_data['designation'],
            district=validated_data['district'],
            state=validated_data['state']
        )
        # Deactivate account until OTP/email verification
        user.is_active = False  
        user.save()
        return user
