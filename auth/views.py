from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth import get_user_model

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