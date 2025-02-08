from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from authentication.models import User
from .models import Investment,
from stockmatching.models import UserProfile
from .serializers import InvestmentSerializer



class InvestmentView(viewsets.ModelViewSet):
    permissions_class = [IsAuthenticated]
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    http_methods = ['get','post','patch','delete']

    #Get Api that returns all the investments of a given User and their info
    @action(detail=False, methods=['get'])
    def get_investments_for_user_id(self, request):
        #check the current request user's ID
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User id is required"}, status=status.HTTP_400_BAD_REQUEST)

        #use the user_id to query for the given user and his profile
        user = get_object_or_404(User, pk=int(user_id))
        user_profile = UserProfile.objects.filter(user=int(user_id)).first()

        if not user_profile:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #gets all of the investments of the user
        investments = Investment.objects.filter(UserProfile=int(user_profile))

        if not investments.exists():
            return Response({"error": "User does not have any investments"}, status=status.HTTP_404_NOT_FOUND)
        
        result = []

        #data of all the investments 
        for Investment in investments:
            InvestmentJson = {
                'stock_symbol': Investment['stock_symbol'],
                'amount_invested': Investment['amount_invested'],
                'time_bought': Investment['time_bought'],
                'price_at_purchase': Investment['price_at_purchase']                
            }
            result.append(InvestmentJson)
        
        return Response(result, status=status.HTTP_200_OK)
    