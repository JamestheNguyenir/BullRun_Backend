from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Sum

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from authentication.models import User
from .models import Investment
from stockmatching.models import UserProfile, StockPrice
from .serializers import InvestmentSerializer
from datetime import timedelta



class InvestmentView(viewsets.ModelViewSet):
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
    
    @action(detail=False, methods=['get'])
    def get_portfolio_value(self, request):
        user_id = request.query_params.get('user_id')
        start_date_str = request.query_params.get('start_date')  # Optional: "YYYY-MM-DD"

        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        investments = Investment.objects.filter(profile=user_profile)

        # Determine date range
        today = now().date()
        default_start_date = today - timedelta(days=365)  # 1 year ago
        start_date = default_start_date if not start_date_str else min(today, max(default_start_date, start_date_str))

        portfolio_history = {}

        # Iterate over each day from start_date to today
        for single_date in (start_date + timedelta(n) for n in range((today - start_date).days + 1)):
            portfolio_value = 0

            for investment in investments:
                # Get stock price for the date (or last known price if unavailable)
                stock_price = StockPrice.objects.filter(stock=investment.stock, date__lte=single_date).order_by('-date').first()

                if stock_price:
                    shares_owned = investment.amount_invested / investment.price_at_purchase
                    portfolio_value += shares_owned * stock_price.price

            # If no investments exist yet, keep value at 0
            portfolio_history[single_date.strftime("%Y-%m-%d")] = portfolio_value

        return Response({"portfolio_value_over_time": portfolio_history}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_portfolio_breakdown(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        investments = Investment.objects.filter(profile=user_profile)

        if not investments.exists():
            return Response({"error": "User does not have any investments"}, status=status.HTTP_404_NOT_FOUND)

        total_investment = investments.aggregate(total=Sum('amount_invested'))['total'] or 0.00

        breakdown = []
        for investment in investments:
            stock = investment.stock
            stock_value = investment.amount_invested  # Assuming this is how the investment is tracked
            proportion = (stock_value / total_investment) * 100 if total_investment > 0 else 0
            breakdown.append({
                'stock_symbol': stock.symbol,
                'stock_name': stock.name,
                'investment_amount': stock_value,
                'proportion': round(proportion, 2)  # Percentage of total investment
            })

        return Response({'total_investment': total_investment, 'investment_breakdown': breakdown}, status=status.HTTP_200_OK)