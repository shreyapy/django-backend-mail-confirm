from django.urls import path
from .views import login, signup, verifyEmail

urlpatterns = [
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('verifyEmail/<str:id>', verifyEmail, name='verifyEmail')
]