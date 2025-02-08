from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from authentication.models import User
from .models import Stock, StockMatch, UserProfile, StockPrice
from .serializers import UserProfileSerializer, StockPriceSerializer, StockSerializer, StockMatchSerializer
# Create your views here.
permission_classes = [IsAuthenticated]

class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_methods = ['get','post','patch','delete']

class StockView(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    http_methods = ['get','post','patch','delete']

class StockMatchView(viewsets.ModelViewSet):
    queryset = StockMatch.objects.all()
    serializer_class = StockMatchSerializer
    
    @action(detail=False, methods=['get'])
    def get_matches_for_user(self,request):
        #check the current request user's ID
        user_id = request.query_params.get('user_id')
        
        ##TODO 
class StockPriceView(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer
    http_methods = ['get','post','patch','delete']

