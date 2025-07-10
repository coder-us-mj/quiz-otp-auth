from django.urls import path
from api.views import SignupViewSet, VerifyOTPViewSet, ResendOTPView, LoginViewSet


# router = routers.DefaultRouter()
# router.register('signup/', SignupViewSet.as_view(), name = 'signup')
# router.register('verify-otp', SignupViewSet.as_view(), name = 'signup')

urlpatterns = [
    path('signup/', SignupViewSet.as_view(), name = 'signup'),
    path('verify-otp/', VerifyOTPViewSet.as_view(), name = 'verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('login/', LoginViewSet.as_view(), name='login'),
]
  
  