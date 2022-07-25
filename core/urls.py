from django.urls import path
from .views import FacilityViews

urlpatterns = [
    path('facility/', FacilityViews.as_view()),
    path('facility/<int:id>', FacilityViews.as_view())
]