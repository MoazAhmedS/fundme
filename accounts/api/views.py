from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountRegisterSerializer, AccountLoginSerializer, ForgotPasswordSerializer
from ..models import ProfileUser
from django.utils.http import urlsafe_base64_decode
from datetime import timedelta
from django.utils.timezone import now

from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny


from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = request.build_absolute_uri(
        reverse('activate-account', kwargs={'uidb64': uid, 'token': token})
    )
    subject = 'Activate Your Account'
    message = f'Hi {user.first_name},\nPlease activate your account using this link:\n{activation_link}'
    send_mail(subject, message, 'your_email@example.com', [user.email])


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountRegisterSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            phone = serializer.validated_data['phone']

            if ProfileUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
            if ProfileUser.objects.filter(phone=phone).exists():
                return Response({"error": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = ProfileUser.create_user(serializer.validated_data)
                send_activation_email(user, request) 

                return Response({
                    "message": "User registered successfully. Please check your email to activate your account.",
                    "user": AccountRegisterSerializer(user).data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = ProfileUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ProfileUser.DoesNotExist):
            user = None
        
        if user:
            if default_token_generator.check_token(user, token):
                token_created_time = user.last_login or user.date_joined
                if now() - token_created_time > timedelta(hours=24):
                    return Response({"error": "Activation link has expired."}, status=status.HTTP_400_BAD_REQUEST)

                if user.email_active:
                    return Response({"message": "Account is already activated."}, status=status.HTTP_200_OK)

                user.email_active = True
                user.save()
                return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid or expired activation link."}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountLoginSerializer(data=request.data)
        print(serializer.is_valid())

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(username=email, password=password)
            if user is not None:
                if not user.email_active:
                    return Response({"error": "Account is not activated."}, status=status.HTTP_403_FORBIDDEN)

                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    def get_response(self):
        user = self.user
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }, status=status.HTTP_200_OK)

    def login(self):
        super().login()
        return self.get_response()
    

def send_reset_password_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = request.build_absolute_uri(
        reverse('reset-password', kwargs={'uidb64': uid, 'token': token})
    )
    subject = 'Reset Your Password'
    message = f'Hi {user.first_name},\nPlease reset your password using this link:\n{reset_link}'
    message += "\nThis link will expire in 1 hour. If you didn't request this, please ignore this email."
    send_mail(subject, message, 'your_email@example.com', [user.email])


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = ProfileUser.objects.get(email=email)
            send_reset_password_email(user, request)
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)