from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from dispo_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('webhook', views.webhook, name='webhook'),
    path('auth/', include('auth.urls')),
    path('send_message/', views.send_message, name='send_message'),

    #path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
]
