from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountRegisterSerializer
from ..models import ProfileUser

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


                return Response({
                    "message": "User registered successfully",
                    "user": AccountRegisterSerializer(user).data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)