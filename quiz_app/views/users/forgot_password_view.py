import random
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.core.cache import cache
from common.response_handler import ResponseHandler  

User = get_user_model()

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return ResponseHandler.handle_400_error("Email is required.")

    try:
        user = User.objects.get(email=email)
        otp = random.randint(100000, 999999)
        cache.set(email, otp, timeout=300)  # Store OTP for 5 minutes

        send_mail(
            'Your Password Reset OTP',
            f'Hello {user.name},\nYour OTP is: {otp}',
            None,
            [email],
            fail_silently=False,
        )

        return ResponseHandler.handle_200_success({
            "message": "OTP sent to email successfully."
        })

    except User.DoesNotExist:
        return ResponseHandler.handle_400_error("User with this email does not exist.")
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)
    
    
@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    if not all([email, otp, new_password]):
        return ResponseHandler.handle_400_error("Email, OTP, and new password are required.")

    cached_otp = cache.get(email)
    if not cached_otp or str(cached_otp) != str(otp):
        return ResponseHandler.handle_400_error("Invalid or expired OTP.")

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        cache.delete(email)

        return ResponseHandler.handle_200_success({
            "message": "Password reset successful."
        })

    except User.DoesNotExist:
        return ResponseHandler.handle_400_error("User not found.")
    except Exception as e:
        return ResponseHandler.handle_500_error(request, e)
    
