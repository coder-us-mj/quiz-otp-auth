from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from api.models import SignUp, EmailOTP
from django.contrib.auth import authenticate
from api.serializers import SignupSerializers, verifyOTPSerializer, ResendOTPSerializer
from api.utils import generate_otp, send_otp_email
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)
# Create your views here.
class SignupViewSet(APIView):
    def post(self, request):
        
        serializer_class = SignupSerializers(data = request.data)
        if serializer_class.is_valid():
            user = serializer_class.save()
            otp = generate_otp()
            cache.set(user.email, otp, timeout=300)
            send_otp_email(user.email, otp)
            EmailOTP.objects.create(email=user.email, otp=otp)
            return Response({"message":"OTP sent to your email. Verify to complete signup."}, status=201)
        else:
            logger.error(f"Serializer errors: {serializer_class.errors}")
            return Response(serializer_class.errors, status=400) 
    
class VerifyOTPViewSet(APIView):
    def post(self, request):
        serializer = verifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].strip()
            otp_input = serializer.validated_data['otp'].strip()

            try:
                otp_record = EmailOTP.objects.filter(email=email).latest('created_at')
            except EmailOTP.DoesNotExist:
                return Response({'error': 'OTP not found. Please request again.'}, status=status.HTTP_404_NOT_FOUND)

            if otp_record.is_expired():
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

            if otp_record.otp != otp_input:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = SignUp.objects.get(email=email)
                user.is_active = True
                user.save()
                otp_record.delete()  # Clean up used OTP
                return Response({'message': 'OTP verified. Account activated.'}, status=status.HTTP_200_OK)
            except SignUp.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResendOTPView(APIView):
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].strip()
            try:
                user = SignUp.objects.get(email=email)
                if user.is_active:
                    return Response({'message': 'User is already verified.'}, status=200)
                
                otp = generate_otp()
                cache.set(email, otp, timeout=300)
                send_otp_email(email, otp)
                EmailOTP.objects.create(email=email, otp=otp)

                return Response({'message': 'OTP resent successfully.'}, status=200)

            except SignUp.DoesNotExist:
                return Response({'error': 'User not found.'}, status=404)

        return Response(serializer.errors, status=400)  
    
    
class LoginViewSet(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Account is not activated. Verify your email OTP.'}, status=403)
        return Response({'error': 'Invalid email or password'}, status=401)  
    
      