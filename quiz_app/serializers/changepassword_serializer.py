from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    Validates current password and ensures new password confirmation.
    """
    current_password = serializers.CharField(write_only=True) # User's existing password
    new_password = serializers.CharField(write_only=True)  # New password to set
    confirm_new_password = serializers.CharField(write_only=True)   # Re-entry of new password for confirmation 

    def validate(self, data):
        """
        Validates the current password and checks if new passwords match.

        Raises:
            ValidationError: If the current password is incorrect or the new passwords don't match.

        Returns:
            dict: Cleaned and validated data
        """
        user = self.context['request'].user

        # Verify current password is correct    
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError({'current_password': 'Current password is incorrect'})

        # Ensure new password and confirm password match
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({'new_password': 'New passwords do not match'})

        return data
