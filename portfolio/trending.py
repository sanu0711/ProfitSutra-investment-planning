from django.shortcuts import render
from dashboard.models import StockData
from django.db.models import F
from django.contrib.auth.decorators import login_required

@login_required(login_url='sign_in')
def trending_view(request):
    undervalued_stocks = StockData.objects.filter(
        pe_ttm_price_to_earnings__lt=15, 
        net_profit_annual_yoy_growth_percent__gt=20, 
        roe_annual_percent__gt=15).order_by('pe_ttm_price_to_earnings').values(
        'stock_name', 'nsecode', 'bsecode', 'current_price', 'pe_ttm_price_to_earnings',
        'net_profit_annual_yoy_growth_percent', 'roe_annual_percent')[0:10]
        
    dividend_yield_stocks = StockData.objects.filter(
        operating_profit_margin_qtr_percent__gt=20, 
        roe_annual_percent__gt=15, 
        net_profit_annual__gt=100).order_by('operating_profit_margin_qtr_percent').values(
        'stock_name', 'nsecode', 'bsecode', 'current_price', 'net_profit_annual',
        'operating_profit_margin_qtr_percent', 'roe_annual_percent','pe_ttm_price_to_earnings')[0:10]
    
    low_debt_high_return_stocks = StockData.objects.filter(
        roe_annual_percent__gt=20, 
        sector_return_on_equity_roe__lt=20).order_by('roe_annual_percent').values(
        'stock_name', 'nsecode', 'bsecode', 'current_price', 'roe_annual_percent',
        'sector_return_on_equity_roe', 'industry_return_on_equity_roe')[0:10]
        
    momentum_stocks = StockData.objects.filter(
        day_volume__gt=2*F('month_volume_avg'), 
        day_sma_50__gt=F('day_sma_200')).order_by('day_volume').values(
        'stock_name', 'nsecode', 'current_price', 'day_sma_50', 'day_sma_200',
        'day_volume', 'month_volume_avg')[0:10]
    
    higher_insider_holdings = StockData.objects.filter(
        promoter_holding_latest_percentage__gt=50, 
        institutional_holding_current_qtr_percentage__gt=20).order_by('institutional_holding_current_qtr_percentage').values(
        'stock_name', 'nsecode', 'bsecode', 'current_price', 'promoter_holding_latest_percentage',
        'institutional_holding_current_qtr_percentage')[0:10]    
    
    low_beta_stocks = StockData.objects.filter(
        beta_1year__lt=1, 
        current_price__gt=F('oneyr_low')+((F('oneyr_high')-F('oneyr_low'))*0.7)).order_by('beta_1year').values(
        'stock_name', 'nsecode', 'current_price', 'beta_1year', 'oneyr_high', 'oneyr_low')[0:10]
        
    support_level_stocks = StockData.objects.filter(
        current_price__range=(F('first_support_s1')*0.95, F('first_support_s1'))).order_by('current_price').values(
        'stock_name', 'nsecode', 'current_price', 'first_support_s1', 'second_support_s2', 'third_support_s3')[0:10]
        
    high_beta_stocks = StockData.objects.filter(
        beta_1year__gt=1.5, 
        day_sma_50__gt=F('day_sma_200')).order_by('beta_1year').values(
        'stock_name', 'nsecode', 'current_price', 'beta_1year', 'day_sma_50', 'day_sma_200')[0:10]
    
    strong_revenue_growth_stocks = StockData.objects.filter(
        revenue_growth_annual_yoy_percent__gt=15, 
        net_profit_annual_yoy_growth_percent__gt=15).order_by('net_profit_annual_yoy_growth_percent').values(
        'stock_name', 'nsecode', 'current_price', 'revenue_growth_annual_yoy_percent', 'net_profit_annual_yoy_growth_percent')[0:10]
           
    top_gainers = StockData.objects.filter(
        day_roc21__gt=10, 
        day_sma_30__gt=F('day_sma_50')).order_by('day_roc21').values(
        'stock_name', 'nsecode', 'current_price', 'day_roc21', 'day_macd', 'day_sma_30', 'day_sma_50')[0:10]
            
    context = {
        'undervalued_stocks': undervalued_stocks,
        'dividend_yield_stocks': dividend_yield_stocks,
        'low_debt_high_return_stocks': low_debt_high_return_stocks,
        'momentum_stocks': momentum_stocks,
        'higher_insider_holdings': higher_insider_holdings,
        'low_beta_stocks': low_beta_stocks,
        'support_level_stocks': support_level_stocks,
        'high_beta_stocks': high_beta_stocks,
        'strong_revenue_growth_stocks': strong_revenue_growth_stocks,
        'top_gainers': top_gainers
    }
    # print(support_level_stocks)
    return render(request, 'trending.html', context)