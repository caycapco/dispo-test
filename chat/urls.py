from django.contrib import admin
from django.urls import path
from chat import views

urlpatterns = [
    #path('test-api/', test_get_api),
    path('test-api/', views.ChatView.as_view(), name="test-api"),

    #path('hello/', views.HelloView.as_view(), name='hello'),
]
