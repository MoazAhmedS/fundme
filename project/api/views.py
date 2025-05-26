from rest_framework.response import Response

from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.pagination import  PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer
from ..models import *

class ReadAndCreateProject(APIView):
    def get(self,request):
        return Response(
            data=ProjectSerializer.getAllProjects(),
            status=status.HTTP_200_OK
        )
    def post(self,request):
        projectSerialized = ProjectSerializer(data=request.data)
        if projectSerialized.is_valid():
            projectSerialized.save()
            return Response(
                data=projectSerialized.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={'errors':projectSerialized.errors
                      },
                status=status.HTTP_400_BAD_REQUEST
            )
        
class ReadUpdateDeleteProjectByID(APIView):
    def get(self,request,id):
        return Response(
            data=ProjectSerializer.getProjectById(id),
            status=status.HTTP_200_OK
        )