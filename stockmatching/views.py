from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from authentication.models import User
from .models import Stock, UserProfile
from .serializers import UserProfileSerializer, StockSerializer

class UserProfileView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_methods = ['get','post','patch','delete']

class StockView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    http_methods = ['get','post','patch','delete']


