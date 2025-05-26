from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountRegisterSerializer
from ..models import ProfileUser
from django.utils.http import urlsafe_base64_decode

from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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
    def generate_unique_username(self, base_name):
        base_name = base_name.lower().replace(" ", "") 
        username = base_name
        counter = 1

        while ProfileUser.objects.filter(username=username).exists():
            username = f"{base_name}{counter}5475"
            counter += 1
        return username
    

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
                first_name = serializer.validated_data['first_name']
                last_name = serializer.validated_data['last_name']
                base_username = f"{first_name}{last_name}"

                username = self.generate_unique_username(base_username)

                user = ProfileUser.create_user(serializer.validated_data, username)
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
        
        if user and default_token_generator.check_token(user, token):
            if( user.email_active):
                return Response({"message": "Account is already activated."}, status=status.HTTP_200_OK)
            user.email_active = True
            user.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)