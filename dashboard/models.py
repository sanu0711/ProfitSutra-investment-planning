from django.db import models

# Create your models here.

class StockData(models.Model):
    stock_name = models.CharField(max_length=200, null=True, blank=True)
    nsecode = models.CharField(max_length=100, null=True, blank=True)
    bsecode = models.FloatField(null=True, blank=True)
    isin = models.CharField(max_length=200, null=True, blank=True)
    industry_name = models.CharField(max_length=200, null=True, blank=True)
    current_price = models.FloatField(null=True, blank=True)
    market_capitalization_in_crores = models.FloatField(null=True, blank=True)
    trendlyne_durability_score = models.FloatField(null=True, blank=True)
    trendlyne_valuation_score = models.FloatField(null=True, blank=True)
    trendlyne_momentum_score = models.FloatField(null=True, blank=True)
    dvm_classification_text = models.CharField(max_length=200, null=True, blank=True)
    prev_day_trendlyne_durability_score = models.FloatField(null=True, blank=True)
    prev_day_trendlyne_valuation_score = models.FloatField(null=True, blank=True)
    prev_day_trendlyne_momentum_score = models.FloatField(null=True, blank=True)
    prev_week_trendlyne_durability_score = models.FloatField(null=True, blank=True)
    prev_week_trendlyne_valuation_score = models.FloatField(null=True, blank=True)
    prev_week_trendlyne_momentum_score = models.FloatField(null=True, blank=True)
    prev_month_trendlyne_durability_score = models.FloatField(null=True, blank=True)
    prev_month_trendlyne_valuation_score = models.FloatField(null=True, blank=True)
    prev_month_trendlyne_momentum_score = models.FloatField(null=True, blank=True)
    normalized_momentum_score = models.FloatField(null=True, blank=True)
    operating_revenue_qtr = models.FloatField(null=True, blank=True)
    net_profit_qtr = models.FloatField(null=True, blank=True)
    revenue_growth_qtr_yoy_percent = models.FloatField(null=True, blank=True)
    net_profit_qtr_growth_yoy_percent = models.FloatField(null=True, blank=True)
    sector_revenue_growth_qtr_yoy_percent = models.FloatField(null=True, blank=True)
    sector_net_profit_growth_qtr_yoy_percent = models.FloatField(null=True, blank=True)
    sector_revenue_growth_qtr_qoq_percent = models.FloatField(null=True, blank=True)
    net_profit_qoq_growth_percent = models.FloatField(null=True, blank=True)
    sector_net_profit_growth_qtr_qoq_percent = models.FloatField(null=True, blank=True)
    operating_profit_margin_qtr_percent = models.FloatField(null=True, blank=True)
    operating_profit_margin_qtr_1yr_ago_percent = models.FloatField(null=True, blank=True)
    operating_revenue_ttm = models.FloatField(null=True, blank=True)
    net_profit_ttm = models.FloatField(null=True, blank=True)
    operating_revenue_annual = models.FloatField(null=True, blank=True)
    net_profit_annual = models.FloatField(null=True, blank=True)
    revenue_growth_annual_yoy_percent = models.FloatField(null=True, blank=True)
    net_profit_annual_yoy_growth_percent = models.FloatField(null=True, blank=True)
    sector_revenue_growth_annual_yoy_percent = models.FloatField(null=True, blank=True)
    cash_from_financing_annual_activity = models.FloatField(null=True, blank=True)
    cash_from_investing_activity_annual = models.FloatField(null=True, blank=True)
    cash_from_operating_activity_annual = models.FloatField(null=True, blank=True)
    net_cash_flow_annual = models.FloatField(null=True, blank=True)
    sector_name = models.CharField(max_length=200, null=True, blank=True)
    latest_financial_result = models.DateTimeField(null=True, blank=True)
    result_announced_date = models.DateTimeField(null=True, blank=True)
    pe_ttm_price_to_earnings = models.FloatField(null=True, blank=True)
    oneyr_forward_forecaster_estimates_pe = models.CharField(max_length=200, null=True, blank=True)
    pe_3yr_average = models.FloatField(null=True, blank=True)
    pe_5yr_average = models.FloatField(null=True, blank=True)
    percent_days_traded_below_current_pe_price_to_earnings = models.FloatField(null=True, blank=True)
    sector_pe_ttm = models.FloatField(null=True, blank=True)
    industry_pe_ttm = models.FloatField(null=True, blank=True)
    peg_ttm_pe_to_growth = models.FloatField(null=True, blank=True)
    oneyr_forward_forecaster_estimates_peg = models.CharField(max_length=200, null=True, blank=True)
    sector_peg_ttm = models.FloatField(null=True, blank=True)
    industry_peg_ttm = models.FloatField(null=True, blank=True)
    price_to_book_value = models.FloatField(null=True, blank=True)
    percent_days_traded_below_current_price_to_book_value = models.FloatField(null=True, blank=True)
    sector_price_to_book_ttm = models.FloatField(null=True, blank=True)
    industry_price_to_book_ttm = models.FloatField(null=True, blank=True)
    basic_eps_ttm = models.FloatField(null=True, blank=True)
    eps_ttm_growth_percent = models.FloatField(null=True, blank=True)
    roe_annual_percent = models.FloatField(null=True, blank=True)
    sector_return_on_equity_roe = models.FloatField(null=True, blank=True)
    industry_return_on_equity_roe = models.FloatField(null=True, blank=True)
    roa_annual_percent = models.FloatField(null=True, blank=True)
    sector_return_on_assets = models.FloatField(null=True, blank=True)
    industry_return_on_assets = models.FloatField(null=True, blank=True)
    piotroski_score = models.FloatField(null=True, blank=True)
    day_mfi = models.FloatField(null=True, blank=True)
    day_rsi = models.FloatField(null=True, blank=True)
    day_macd = models.FloatField(null=True, blank=True)
    day_macd_signal_line = models.FloatField(null=True, blank=True)
    day_sma_30 = models.FloatField(null=True, blank=True)
    day_sma_50 = models.FloatField(null=True, blank=True)
    day_sma_100 = models.FloatField(null=True, blank=True)
    day_sma_200 = models.FloatField(null=True, blank=True)
    day_sma_5 = models.FloatField(null=True, blank=True)
    day_ema_12 = models.FloatField(null=True, blank=True)
    day_ema_20 = models.FloatField(null=True, blank=True)
    day_ema_50 = models.FloatField(null=True, blank=True)
    day_ema_100 = models.FloatField(null=True, blank=True)
    beta_1month = models.FloatField(null=True, blank=True)
    beta_3month = models.FloatField(null=True, blank=True)
    beta_1year = models.FloatField(null=True, blank=True)
    beta_3year = models.FloatField(null=True, blank=True)
    day_roc21 = models.FloatField(null=True, blank=True)
    day_roc125 = models.FloatField(null=True, blank=True)
    day_atr = models.FloatField(null=True, blank=True)
    day_adx = models.FloatField(null=True, blank=True)
    pivot_point = models.FloatField(null=True, blank=True)
    first_resistance_r1 = models.FloatField(null=True, blank=True)
    first_resistance_r1_to_price_diff_percent = models.FloatField(null=True, blank=True)
    second_resistance_r2 = models.FloatField(null=True, blank=True)
    second_resistance_r2_to_price_diff_percent = models.FloatField(null=True, blank=True)
    third_resistance_r3 = models.FloatField(null=True, blank=True)
    third_resistance_r3_to_price_diff_percent = models.FloatField(null=True, blank=True)
    first_support_s1 = models.FloatField(null=True, blank=True)
    first_support_s1_to_price_diff_percent = models.FloatField(null=True, blank=True)
    second_support_s2 = models.FloatField(null=True, blank=True)
    second_support_s2_to_price_diff_percent = models.FloatField(null=True, blank=True)
    third_support_s3 = models.FloatField(null=True, blank=True)
    third_support_s3_to_price_diff_percent = models.FloatField(null=True, blank=True)
    day_low = models.FloatField(null=True, blank=True)
    day_high = models.FloatField(null=True, blank=True)
    week_low = models.FloatField(null=True, blank=True)
    week_high = models.FloatField(null=True, blank=True)
    month_low = models.FloatField(null=True, blank=True)
    month_high = models.FloatField(null=True, blank=True)
    qtr_low = models.FloatField(null=True, blank=True)
    qtr_high = models.FloatField(null=True, blank=True)
    oneyr_low = models.FloatField(null=True, blank=True)
    oneyr_high = models.FloatField(null=True, blank=True)
    day_volume = models.FloatField(null=True, blank=True)
    week_volume_avg = models.FloatField(null=True, blank=True)
    month_volume_avg = models.FloatField(null=True, blank=True)
    threemonth_volume_avg = models.FloatField(null=True, blank=True)
    sixmonth_volume_avg = models.FloatField(null=True, blank=True)
    year_volume_avg = models.FloatField(null=True, blank=True)
    consolidated_end_of_day_volume = models.FloatField(null=True, blank=True)
    consolidated_previous_end_of_day_volume = models.FloatField(null=True, blank=True)
    consolidated_5day_average_end_of_day_volume = models.FloatField(null=True, blank=True)
    consolidated_30day_average_end_of_day_volume = models.FloatField(null=True, blank=True)
    consolidated_6m_average_end_of_day_volume = models.FloatField(null=True, blank=True)
    day_volume_multiple_of_week = models.FloatField(null=True, blank=True)
    vol_day_times_vol_week_strong = models.CharField(max_length=100, null=True, blank=True)
    consolidated_day_volume = models.FloatField(null=True, blank=True)
    vwap_day = models.FloatField(null=True, blank=True)
    promoter_holding_latest_percentage = models.FloatField(null=True, blank=True)
    promoter_holding_change_qoq_percentage = models.FloatField(null=True, blank=True)
    promoter_holding_change_4qtr_percentage = models.FloatField(null=True, blank=True)
    promoter_holding_change_8qtr_percentage = models.FloatField(null=True, blank=True)
    promoter_holding_pledge_percentage_qtr = models.FloatField(null=True, blank=True)
    promoter_pledge_change_qoq_percent = models.FloatField(null=True, blank=True)
    mf_holding_current_qtr_percentage = models.FloatField(null=True, blank=True)
    mf_holding_change_qoq_percentage = models.FloatField(null=True, blank=True)
    mf_holding_change_1month_percentage = models.FloatField(null=True, blank=True)
    mf_holding_change_2month_percentage = models.FloatField(null=True, blank=True)
    mf_holding_change_3month_percentage = models.FloatField(null=True, blank=True)
    mf_holding_change_4qtr_percentage = models.FloatField(null=True, blank=True)
    mf_holding_change_8qtr_percentage = models.FloatField(null=True, blank=True)
    fii_holding_current_qtr_percentage = models.FloatField(null=True, blank=True)
    fii_holding_change_qoq_percentage = models.FloatField(null=True, blank=True)
    fii_holding_change_4qtr_percentage = models.FloatField(null=True, blank=True)
    fii_holding_change_8qtr_percentage = models.FloatField(null=True, blank=True)
    institutional_holding_current_qtr_percentage = models.FloatField(null=True, blank=True)
    institutional_holding_change_qoq_percentage = models.FloatField(null=True, blank=True)
    institutional_holding_change_4qtr_percentage = models.FloatField(null=True, blank=True)
    institutional_holding_change_8qtr_percentage = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.stock_name
    class Meta:
        db_table = 'stockdata'
        managed = True
        verbose_name = 'Stock Data'
        verbose_name_plural = 'Stock Data'
        