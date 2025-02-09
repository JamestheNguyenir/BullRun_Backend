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
from stockmatching.models import UserProfile
from .serializers import InvestmentSerializer
from datetime import datetime,timedelta
import yfinance as yf

from decimal import Decimal  # Import Decimal for conversion

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
        default_start_date = today - timedelta(days=30)  
        start_date = default_start_date if not start_date_str else min(
            today, max(default_start_date, datetime.strptime(start_date_str, "%Y-%m-%d").date())
        )

        portfolio_history = {}
        last_known_prices = {}  # Dictionary to store the last known prices

        # Iterate over each day from start_date to today
        for single_date in (start_date + timedelta(n) for n in range((today - start_date).days + 1)):
            portfolio_value = Decimal(0)  # Initialize as Decimal

            for investment in investments:
                ticker = investment.stock.symbol  
                stock_data = yf.Ticker(ticker)

                # Fetch historical data up to the current date in the loop
                hist = stock_data.history(start=single_date, end=single_date + timedelta(days=1))

                if not hist.empty:
                    # Get the closing price for the specific date and update the last known price
                    closing_price = Decimal(str(hist['Close'].iloc[0]))  
                    last_known_prices[ticker] = closing_price  # Store latest price
                else:
                    # If no price is found, use the last known price (if available)
                    closing_price = last_known_prices.get(ticker, Decimal(0))  

                # Calculate portfolio value
                shares_owned = investment.amount_invested / investment.price_at_purchase
                portfolio_value += shares_owned * closing_price

            # Store the portfolio value for the date
            portfolio_history[single_date.strftime("%Y-%m-%d")] = float(portfolio_value)

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

        # Dictionary to store aggregated data for each stock
        stock_breakdown = {}

        # Cache for current prices to avoid redundant API calls
        current_prices = {}

        for investment in investments:
            ticker = investment.stock.symbol

            # Fetch current price for the stock
            if ticker not in current_prices:
                stock_data = yf.Ticker(ticker)
                hist = stock_data.history(period="1d")
                if not hist.empty:
                    current_price = Decimal(str(hist['Close'].iloc[-1]))
                else:
                    current_price = Decimal('0')
                current_prices[ticker] = current_price

            # Calculate current value of the investment
            shares_owned = investment.amount_invested / investment.price_at_purchase
            current_value = shares_owned * current_prices[ticker]

            # Aggregate data for the stock
            if ticker not in stock_breakdown:
                stock_breakdown[ticker] = {
                    'stock_symbol': ticker,
                    'stock_name': investment.stock.name,
                    'total_invested': Decimal(0),
                    'total_current_value': Decimal(0),
                    'shares_owned': Decimal(0)
                }

            stock_breakdown[ticker]['total_invested'] += investment.amount_invested
            stock_breakdown[ticker]['total_current_value'] += current_value
            stock_breakdown[ticker]['shares_owned'] += shares_owned

        # Calculate total portfolio value
        total_invested = sum(item['total_invested'] for item in stock_breakdown.values())
        total_current_value = sum(item['total_current_value'] for item in stock_breakdown.values())

        # Prepare the breakdown for response
        breakdown = []
        for stock_data in stock_breakdown.values():
            proportion = (stock_data['total_current_value'] / total_current_value) * 100 if total_current_value > 0 else 0
            breakdown.append({
                'stock_symbol': stock_data['stock_symbol'],
                'stock_name': stock_data['stock_name'],
                'total_invested': float(stock_data['total_invested']),
                'total_current_value': float(stock_data['total_current_value']),
                'shares_owned': float(stock_data['shares_owned']),
                'proportion': round(proportion, 2)  # Percentage of total portfolio
            })

        # Calculate total gains (current value - initial investment)
        total_gains = total_current_value - total_invested

        return Response({
            'total_invested': float(total_invested),
            'total_current_value': float(total_current_value),
            'total_gains': float(total_gains),
            'investment_breakdown': breakdown
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_leaderboard(self, request):

        # Retrieve all user profiles.
        all_profiles = UserProfile.objects.all()

        # Dictionary to cache current prices for tickers (to reduce repeated yfinance calls)
        current_prices = {}

        leaderboard = []
        for profile in all_profiles:
            investments = Investment.objects.filter(profile=profile)
            if not investments.exists():
                continue  # Skip profiles with no investments

            total_invested = Decimal(0)
            total_current_value = Decimal(0)
            for investment in investments:
                ticker = investment.stock.symbol

                # Cache current price per ticker.
                if ticker not in current_prices:
                    stock_data = yf.Ticker(ticker)
                    hist = stock_data.history(period="1d")
                    if not hist.empty:
                        price = Decimal(str(hist['Close'].iloc[-1]))
                    else:
                        price = Decimal('0')
                    current_prices[ticker] = price

                shares_owned = investment.amount_invested / investment.price_at_purchase
                current_price = current_prices[ticker]

                total_invested += investment.amount_invested
                total_current_value += shares_owned * current_price

            if total_invested > 0:
                percentage_gain = ((total_current_value - total_invested) / total_invested) * 100
            else:
                percentage_gain = Decimal(0)

            leaderboard.append({
                'user_id': profile.user.id,
                'name': profile.user.name,
                'percentage_gain': float(round(percentage_gain, 2)),
                'total_invested': float(total_invested),
                'total_current_value': float(total_current_value)
            })

        # Sort the leaderboard by percentage gain in descending order.
        leaderboard.sort(key=lambda x: x['percentage_gain'], reverse=True)

        return Response({"leaderboard": leaderboard}, status=status.HTTP_200_OK)