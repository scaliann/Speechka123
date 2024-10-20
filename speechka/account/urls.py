from django.urls import path

from .views import *


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('sessions/', SessionList.as_view(), name='session_list'),
    path('session/<int:session>/', SessionDetail.as_view(), name='session_detail'),


]




