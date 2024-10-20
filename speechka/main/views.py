from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import *
from account.models import User
class HomeView(TemplateView):
    template_name = 'home.html'


