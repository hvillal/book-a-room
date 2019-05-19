from django.urls import path
from .views import HomePageView

urlpatterns = [
    # Página de inicio
    path('', HomePageView.as_view(), name='home'),
]
