from rest_framework import serializers
from api.models import SignUp
from django.contrib.auth.password_validation import validate_password

class SignupSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = SignUp
        fields = ['name', 'email', 'designation', 'phone', 'district', 'state', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['password'])  # Django's built-in validator
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = SignUp.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            designation=validated_data['designation'],
            district=validated_data['district'],
            state=validated_data['state']
        )
        user.is_active = False  # Deactivate until OTP verification
        user.save()
        return user

class verifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length = 6)
    

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    