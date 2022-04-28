from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from dispo_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('webhook', views.webhook, name='webhook'),
]
