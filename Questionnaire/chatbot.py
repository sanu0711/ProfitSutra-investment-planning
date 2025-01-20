
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from decimal import Decimal
from dashboard.models import StockData
from django.db import connection
import os
from dotenv import load_dotenv
load_dotenv()

model_name = "gemini-1.5-pro"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def convert_to_float(data):
    if isinstance(data, list):
        return [convert_to_float(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(convert_to_float(item) for item in data)
    elif isinstance(data, Decimal):
        return float(data)  
    return data

chat_model = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    convert_system_message_to_human=True
)

def query_p(user_input):
    query_prompt = PromptTemplate(
        input_variables=["user_input"],
        template=(
            """
    You are an AI that converts natural language into MySQL queries for filtering stocks. Given the following columns and description of column  in the table 'StockDatanew' so you need to always use FROM stockdata :
    1. stock_name: The name of the listed company. Used to identify the organization behind the stock
    2. nsecode: Unique ticker code for the stock on the National Stock Exchange. Helps locate the stock quickly.
    3. bsecode: Unique ticker code for the stock on the Bombay Stock Exchange. Identifies the stock for trading on BSE.
    4. isin: International Securities Identification Number assigned to each stock. Standardized globally for trading 
    5. industry_name: The sector or category the company operates in. Used for benchmarking and sector analysis
    6. current_price: The most recent price at which the stock was traded. Indicates its current market valuation
    7. market_capitalization_in_crores: The total market value of all outstanding shares of the company. Reflects company size
    8. trendlyne_durability_score: A score representing the company’s financial stability. Based on parameters like debt and earnings
    9. trendlyne_valuation_score: Score evaluating the stock’s relative valuation. Helps identify overvalued or undervalued stocks
    10. trendlyne_momentum_score: Score based on price momentum. Indicates whether the stock is gaining or losing value
    11. dvm_classification_text: Classification of the stock’s durability, valuation, and momentum. Useful for holistic assessment.
    12. Prev_Day_trendlyne_durability_score: Stability score from the previous trading day. Used to track changes in financial health.
    13. Prev_Day_trendlyne_valuation_score: Stock valuation score from the previous trading day. Indicates short-term value trends.
    14. Prev_Day_trendlyne_momentum_score: Price momentum score from the previous day. Highlights daily momentum shifts.
    15. Prev_Week_trendlyne_durability_score: Durability score from the previous week. Useful for weekly trend analysis.
    16. Prev_Week_trendlyne_valuation_score: Valuation score from a week ago. Tracks changes in the stock’s value assessment
    17. Prev_Week_trendlyne_momentum_score: Momentum score from the previous week. Shows short-term price movement trends.
    18. Prev_Month_trendlyne_durability_score: Durability score as of the prior month. Evaluates stability over a longer horizon
    19. Prev_Month_trendlyne_valuation_score: Valuation score from a month ago. Compares current vs. past valuations.
    20. Prev_Month_trendlyne_momentum_score: Momentum score from the prior month. Useful for medium-term momentum tracking.
    21. normalized_momentum_score: Adjusted score measuring price momentum. Filters out market anomalies for clarity.
    22. operating_revenue_qtr: Total revenue generated during the quarter. Key indicator of business activity and scale.
    23. net_profit_qtr: Profit after all expenses during the quarter. Reflects company’s quarterly profitability.
    24. revenue_growth_qtr_yoy_percent: Year-on-year percentage growth in quarterly revenue. Measures business growth rate
    25. net_profit_qtr_Growth_YoY_Percent: Year-on-year growth percentage in quarterly profits. Tracks profitability improvements
    26. Sector_revenue_growth_qtr_yoy_percent: Revenue growth of the entire sector YoY. Benchmarks the company within its sector.
    27. sector_net_profit_growth_qtr_yoy_percent: Sector-wide YoY net profit growth. Indicates industry-wide profit trends.
    28. sector_revenue_growth_qtr_qoq_percent: Quarter-on-quarter revenue growth of the sector. Highlights seasonal variations.
    29. net_profit_qoq_growth_percent: Quarter-on-quarter profit growth. Useful for detecting recent profitability changes.
    30. sector_net_profit_growth_qtr_qoq_percent: Profit growth of the sector QoQ. Helps compare company vs. sector performance.
    31. operating_profit_margin_qtr_percent: The operating profit margin percentage for the last quarter. Indicates operational efficiency.
    32. operating_profit_margin_qtr_1yr_ago_percent: The operating profit margin percentage from the same quarter last year. For historical comparison.
    33. operating_revenue_ttm: Trailing twelve-month revenue. Useful for assessing long-term financial performance.
    34. net_profit_ttm: Trailing twelve-month net profit. Indicates long-term profitability trends.
    35. operating_revenue_annual: Revenue generated annually. Reflects the overall financial size of the business.
    36. net_profit_annual: Annual net profit achieved. Indicates company’s overall annual profitability
    37. revenue_growth_annual_yoy_percent: Year-over-year annual revenue growth percentage. Shows yearly business growth.
    38. net_profit_annual_YoY_Growth_Percent: Annual net profit growth percentage year-over-year. Highlights long-term trends.
    39  Sector_revenue_growth_annual_yoy_percent: Year-over-year annual revenue growth percentage for the sector. Provides sectoral context.
    40. cash_from_financing_annual_activity: Cash generated or used in financing activities over the year. Reflects capital structure decisions. 
    41. cash_from_investing_activity_annual: Cash generated or used in investing activities annually. Indicates investment strategy. 
    42. cash_from_operating_activity_annual: Cash generated or used in operating activities annually. Shows operational cash flow. 
    43  net_cash_flow_annual: Net cash flow for the year. Represents overall liquidity and financial health
    44  sector_name: The name of the industry sector to which the company belongs. Helps categorize and benchmark performance within a specific sector.
    45  latest_financial_result: Represents the most recent financial results reported by the company, such as quarterly or annual data. Reflects the latest performance metrics.
    46  result_announced_date: The date on which the company announced its latest financial results. Useful for tracking reporting timelines and market reactions
    47  pe_ttm_price_to_earnings: The price-to-earnings ratio calculated based on trailing twelve months (TTM) earnings. Indicates how much investors are willing to pay per unit of earnings.
    48  oneyr_forward_forecaster_estimates_pe: The projected price-to-earnings ratio for the next year, based on forecaster estimates. Reflects expectations for future growth and profitability.
    49  pe_3yr_average: The average price-to-earnings ratio over the last three years. Provides a historical perspective on valuation trends.
    50  pe_5yr_average: The average price-to-earnings ratio over the past five years. Offers a longer-term view of valuation consistency
    51. percent_days_traded_below_current_pe_price_to_earnings: The percentage of trading days where the stock's PE ratio was below its current PE. Indicates the rarity or frequency of the current valuation level.
    52. sector_pe_ttm: The trailing twelve-month price-to-earnings ratio averaged across all companies in the sector. Helps compare the company's valuation to its peers.
    53. industry_pe_ttm: The trailing twelve-month price-to-earnings ratio averaged across companies in the industry. Provides a more granular comparison relative to specific competitors.
    54. peg_ttm_pe_to_growth: The price-to-earnings-to-growth ratio based on TTM earnings. Combines valuation with growth to indicate how much investors are paying for future growth.
    55. oneyr_forward_forecaster_estimates_peG: The projected PEG ratio for the next year, based on forecaster estimates. Reflects expectations of future valuation efficiency.
    56. sector_peg_ttm: The average PEG ratio for the sector based on trailing twelve months. Indicates growth-adjusted valuations across the sector.
    57. industry_peg_ttm: The average PEG ratio for the industry based on trailing twelve months. Provides a more specific growth-adjusted valuation benchmark.
    58. price_to_book_value: The ratio of the stock price to its book value per share. Indicates how the market values the company relative to its net asset value.
    59. Percent_Days_Traded_Below_current_price_to_Book_Value: The percentage of trading days where the stock's price-to-book ratio was below its current level. Highlights how often the current valuation is exceeded
    60. sector_price_to_book_ttm: The trailing twelve-month price-to-book ratio averaged across all companies in the sector. Helps assess relative valuation within the sector.
    61. industry_price_to_book_ttm: The trailing twelve-month price-to-book ratio averaged across all companies in the industry. Provides an industry-specific valuation comparison.
    62. basic_eps_ttm: The basic earnings per share over the trailing twelve months. Reflects the profitability allocated to each outstanding share.
    63. eps_ttm_growth_percent: The percentage growth in earnings per share over the trailing twelve months. Indicates improvement or decline in profitability.
    64. roe_annual_percent: The annual return on equity (ROE) expressed as a percentage. Measures profitability relative to shareholders' equity.
    65. sector_return_on_equity_roe: The average annual return on equity for all companies in the sector. Helps benchmark the company’s performance within its sector.
    66. industry_return_on_equity_roe: The average annual return on equity for all companies in the industry. Provides a narrower benchmark within specific industry peers.
    67. roa_annual_percent: The annual return on assets (ROA) expressed as a percentage. Reflects how efficiently the company uses its assets to generate profit.
    68. sector_return_on_assets: The average annual return on assets across all companies in the sector. A benchmark for operational efficiency within the sector
    69. industry_return_on_assets: The average annual return on assets across all companies in the industry. Indicates efficiency compared to direct competitors.
    70. piotroski_score: A score based on nine financial criteria that measure a company’s financial strength and growth potential. Indicates the overall health of the company.
    71. day_mfi: The Money Flow Index for the day, calculated based on price and volume data. Used to measure buying and selling pressure.
    72. day_rsi: The Relative Strength Index for the day, indicating whether the stock is overbought or oversold on a scale of 0 to 100.
    73. day_macd: The Moving Average Convergence Divergence for the day. Highlights the relationship between two moving averages of the stock's price.
    74. day_macd_Signal_Line: The signal line for the MACD, used to generate buy or sell signals when it crosses the MACD line.
    75. day_sma_30: The 30-day Simple Moving Average of the stock's price. Indicates the average closing price over the last 30 days.
    76. day_sma_50: The 50-day Simple Moving Average of the stock's price. A mid-term trend indicator often used by traders.
    77. day_sma_100: The 100-day Simple Moving Average of the stock's price. Represents a longer-term trend of the stock.
    78. day_sma_200: The 200-day Simple Moving Average of the stock's price. A key indicator of long-term trends.
    79. day_sma_5: The 5-day Simple Moving Average of the stock's price. Represents short-term price trends.
    80. day_ema_12: The 12-day Exponential Moving Average of the stock's price. Gives more weight to recent prices for identifying trends.
    81. day_ema_20: The 20-day Exponential Moving Average of the stock's price. Used to track short to medium-term trends.
    82. day_ema_50: The 50-day Exponential Moving Average of the stock's price. Highlights mid-term momentum.
    83. day_ema_100: The 100-day Exponential Moving Average of the stock's price. Focuses on long-term trend analysis.
    84. beta_1month: The beta coefficient over the last one month, measuring the stock's volatility relative to the market.
    85. beta_3month: The beta coefficient over the last three months. Reflects short-term market risk exposure.
    86. beta_1year: The beta coefficient over the last one year. Indicates the stock's volatility relative to the broader market over the medium term.
    87. beta_3year: The beta coefficient over the last three years. Captures long-term market risk trends for the stock.
    88. day_roc21: The Rate of Change (ROC) over 21 days, measuring the percentage change in the stock's price over this period.
    89. day_roc125: The Rate of Change (ROC) over 125 days, providing a long-term momentum indicator for the stock.
    90. day_atr: The Average True Range for the day, showing the average volatility of the stock.
    91. day_adx: The Average Directional Index for the day. Measures the strength of the stock's trend.
    92. pivot_point: The pivot point calculated for the day, used to identify potential support and resistance levels.
    93. first_resistance_r1: The first level of resistance for a stock, indicating a price point where selling interest may emerge, potentially preventing further price increases.
    94. first_resistance_r1_to_Price_Diff_Percent: The percentage difference between the current price and the first resistance level, providing insight into the proximity of the price to this resistance.
    95. second_resistance_r2: The second level of resistance, representing a higher price point where additional selling pressure may occur.
    96. second_resistance_r2_to_Price_Diff_Percent: The percentage difference between the current price and the second resistance level, indicating the distance to this key price point
    97. third_resistance_r3: The third level of resistance, a further price point that may present significant barriers to upward movement.
    98. third_resistance_r3_to_Price_Diff_Percent: The percentage difference between the current price and the third resistance level, showing how far the price is from this level.
    99. first_support_s1: The first level of support for a stock, indicating a price point where buying interest may emerge, potentially preventing further price declines.
    100. first_support_s1_to_Price_Diff_Percent: The percentage difference between the current price and the first support level, highlighting the proximity to this support
    101. second_support_s2: The second level of support, representing a deeper price point where additional buying pressure may occur.
    102. second_support_s2_to_Price_Diff_Percent: The percentage difference between the current price and the second support level, indicating the distance to this critical price point.
    103. third_support_s3: The third level of support, a further price point that may provide significant buying interest.
    104. third_support_s3_to_Price_Diff_Percent: The percentage difference between the current price and the third support level, showing how far the price is from this support.
    105. day_low: The lowest price of the stock during the current trading day.
    106. day_high: The highest price of the stock during the current trading day
    107. week_low: The lowest price of the stock during the current week.
    108. week_high: The highest price of the stock during the current week.
    109. month_low: The lowest price of the stock during the current month.
    110. month_high: The highest price of the stock during the current month
    111. qtr_low: The lowest price of the stock during the current quarter.
    112. qtr_high: The highest price of the stock during the current quarter.
    113. oneyr_low: The lowest price of the stock over the past year.
    114. oneyr_high: The highest price of the stock over the past year.
    115. day_volume: The total trading volume of the stock for the current trading day, indicating the number of shares traded.
    116. week_volume_avg: The average trading volume of the stock over the current week, providing insight into typical trading activity
    117. month_volume_avg: The average trading volume of the stock over the current month, indicating broader trends in trading activity.
    118. Threemonth_volume_avg: The average trading volume of the stock over the past three months, useful for assessing changes in interest and activity over time.
    119. Sixmonth_volume_avg: The average trading volume of the stock over the past six months, highlighting medium-term trends in trading volume.
    120. year_volume_avg: The average trading volume of the stock over the past year, reflecting long-term trading activity patterns.
    121. Consolidated_End_of_day_volume: The total trading volume at the end of the trading day, combining all trading activity for that day.
    122. Consolidated_Previous_End_of_day_volume: The total trading volume at the end of the previous trading day, useful for comparison with the current day’s volume.
    123. Consolidated_5Day_Average_End_of_day_volume: The average end-of-day trading volume over the past five trading days, providing insight into recent trading trends.
    124. Consolidated_30Day_Average_End_of_day_volume: The average end-of-day trading volume over the past 30 trading days, indicating the longer-term trading activity.
    125. Consolidated_6M_Average_End_of_day_volume: The average end-of-day trading volume over the past six months, useful for assessing shifts in trading patterns.
    126. day_volume_Multiple_of_Week: A metric showing how the current day's trading volume compares to the weekly average, indicating whether the day is experiencing unusually high or low activity.
    127. vol_day_times_vol_week_strong: A measure indicating whether the current day's volume is significantly stronger than the weekly average, suggesting heightened interest or trading activity.
    128. consolidated_day_volume: The total trading volume for the day across all exchanges or platforms, providing a comprehensive view of trading activity
    129. vwap_day: The Volume-Weighted Average Price for the stock on the current trading day, representing the average price at which shares were traded, weighted by volume.
    130. promoter_holding_latest_percentage: The most recent percentage of shares held by promoters, indicating their stake in the company.
    131. promoter_holding_change_qoq_percentage: The percentage change in promoter holdings from the previous quarter, reflecting shifts in promoter confidence or strategy.
    132. promoter_holding_change_4qtr_percentage: The percentage change in promoter holdings over the past four quarters, useful for evaluating longer-term trends in promoter ownership.
    133. promoter_holding_change_8qtr_percentage: The percentage change in promoter holdings over the past eight quarters, indicating more extended trends in promoter involvement.
    134. promoter_holding_pledge_percentage_qtr: The percentage of promoter-held shares that are pledged as collateral for loans, reflecting potential financial risk
    135. promoter_pledge_change_qoq_percent: The percentage change in the pledged promoter shares from the previous quarter, indicating changes in financial leverage or risk exposure.
    136. mf_holding_current_qtr_percentage: The percentage of shares held by mutual funds in the current quarter, indicating the level of institutional interest from mutual funds.
    137. mf_holding_change_qoq_percentage: The percentage change in mutual fund holdings from the previous quarter, reflecting trends in mutual fund investment activity.
    138. mf_holding_change_1month_percentage: The percentage change in mutual fund holdings over the past month, highlighting recent shifts in investment patterns.
    139. mf_holding_change_2month_percentage: The percentage change in mutual fund holdings over the past two months, providing insight into short-term trends in mutual fund investments.
    140. mf_holding_change_3month_percentage: The percentage change in mutual fund holdings over the past three months, indicating medium-term trends in mutual fund participation.
    141. mf_holding_change_4qtr_percentage: The percentage change in mutual fund holdings over the past four quarters, useful for assessing longer-term investment trends.
    142. mf_holding_change_8qtr_percentage: The percentage change in mutual fund holdings over the past eight quarters, indicating extended trends in mutual fund investments.
    143. fii_holding_current_qtr_percentage: The percentage of shares held by foreign institutional investors in the current quarter, reflecting international investment interest.
    144. fii_holding_change_qoq_percentage: The percentage change in FII holdings from the previous quarter, indicating shifts in foreign institutional investment behavior.
    145. fii_holding_change_4qtr_percentage: The percentage change in FII holdings over the past four quarters, providing insights into long-term trends in foreign investment.
    146. fii_holding_change_8qtr_percentage: The percentage change in FII holdings over the past eight quarters, indicating extended trends in foreign institutional investment.
    147. institutional_holding_current_qtr_percentage: The total percentage of shares held by all institutional investors in the current quarter, indicating overall institutional interest.
    148. institutional_holding_change_qoq_percentage: The percentage change in institutional holdings from the previous quarter, reflecting changes in institutional investment activity.
    149. institutional_holding_change_4qtr_percentage: The percentage change in institutional holdings over the past four quarters, useful for assessing longer-term institutional trends.
    150. institutional_holding_change_8qtr_percentage: The percentage change in institutional holdings over the past eight quarters, indicating extended trends in institutional ownership.
    Important guidelines:
    1. Always include the 'stockdata' table in the query.
    2. Ensure the query is compatible with MySQL's 'ONLY_FULL_GROUP_BY' mode by:
    - Including all non-aggregated columns in the GROUP BY clause.
    - Using aggregate functions like MAX, MIN, AVG, SUM for columns not included in GROUP BY.
    3. If the query involves retrieving specific rows (e.g., the row corresponding to the maximum or minimum value of a column):
    - Use subqueries to find the maximum or minimum value and filter rows accordingly.
    - Alternatively, use window functions (if supported) to rank rows and filter the top-ranked ones.
    4. For ranking or retrieving the top results within groups, prefer window functions such as RANK() or ROW_NUMBER() in MySQL 8.0+.
    5. For selecting columns like 'stock_name' along with aggregated values, ensure the query logic includes either a subquery or window function to avoid conflicts with ONLY_FULL_GROUP_BY.
    6. Avoid common SQL syntax issues and ensure all column names, conditions, and clauses are valid for MySQL.
    7. show only revelent columns in the output based on the user input .
    8. this data will be shown to the user so give a good name to column using sql Allias like stock_name AS Stock Name,market_capitalization_in_crores AS Market Capitalization (in crores) etc.
    Transform the following user input into a valid SQL query:

    User Input: {user_input}

    Output only the SQL query without any additional text, including the database name for example:- 'SELECT Stock FROM stockdata ORDER BY MarketCap DESC'
    """
        )
    )
    return query_prompt

def execute_sql_query(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return {
                "columns": column_names,
                "data": results
            }
    except Exception as e:
        return f"Error executing query: {str(e)}"

def chat_to_query(user_input):
    try:
        query_prompt = query_p(user_input)
        chain = LLMChain(llm=chat_model, prompt=query_prompt)
        sql_query = chain.run(user_input)
        sql_query = sql_query.replace("```sql\n", "").replace("```", "").strip()
        print(f"\nGenerated SQL Query:\n{sql_query}")
        result = execute_sql_query(sql_query)
        return result
    except Exception as e:
        return str(e)
