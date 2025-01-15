from django.shortcuts import render,redirect
from .models import Portfolio, UserStock, recommStock
from django.contrib.auth.decorators import login_required
from dashboard.models import StockData
import requests
import json

# Create your views here.


def recom_helper():
    data = []
    tickers = ['20MICRONS','360ONE','3MINDIA','INFOLLION','TDPOWERSYS']
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    recommStock.objects.all().delete()
    for ticker in tickers:
        
        url = f"http://20.197.4.173/stock_details/{ticker}"
        response = requests.get(url, headers=headers)
        data.append(json.loads(response.json()))
        recomm = recommStock.objects.create(ticker=ticker, jsondata=json.loads(response.json()))
        recomm.save()
       
    return data

@login_required(login_url='sign_in') 
def portfolio_view(request):
    user = request.user
    portfolio, created = Portfolio.objects.get_or_create(user=user)
    if created:
        portfolio.save()
    stock_names_option = StockData.objects.values_list('stock_name', flat=True)
    user_stocks = portfolio.stocks.all()
    # recom = recom_helper()
    recom = []
    db_recom = recommStock.objects.all()
    for rec in db_recom:
        recom.append(rec.jsondata)
        
    return render(request, 'portfolio.html', {
        'portfolio': portfolio,
        'stock_names_option': stock_names_option,
        'user_stocks': user_stocks,
        'recom': recom,
        })

@login_required(login_url='sign_in') 
def update_create_portfolio(request):
    user = request.user
    portfolio, created = Portfolio.objects.get_or_create(user=user)
    if created:
        portfolio.save()
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        buy_date = request.POST.get('buy_date')
        stock = UserStock.objects.create(name=name, price=price, quantity=quantity, buy_date=buy_date)
        stock.save()
        portfolio.stocks.add(stock)
        portfolio.save()
    return redirect('portfolio')