from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.forms.models import model_to_dict

#generates token for authentication
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

#register new user to the system
class RegisterView(generics.CreateAPIView):
	User = get_user_model()
	queryset = User.objects.all()
	permission_classes = (AllowAny,)
	serializer_class = RegisterSerializer

class LoggedInUserView(APIView):
    def get(self, request):
    	User = get_user_model()
    	print(request.user.email)
    	queryset = User.objects.get(email=request.user.email)
    	return JsonResponse({"current_user": model_to_dict(queryset)})