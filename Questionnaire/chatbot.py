# import json
# Create your tests here.
# from mysql.connector import connect, Error
# from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from decimal import Decimal
# Database Configuration
# db_config = {
#     'host': 'mysqlserver1235.mysql.database.azure.com',
#     'database': 'stock_database',
#     'user': 'mysqladmin',
#     'password': 'Khajanchi123',
#     # 'ssl_ca': r"C:\Users\Abhishek Saraswat\Downloads\DigiCertGlobalRootG2.crt.pem"
# }
# def convert_to_float(data):
#     if isinstance(data, list):
#         return [convert_to_float(item) for item in data]
#     elif isinstance(data, tuple):
#         return tuple(convert_to_float(item) for item in data)
#     elif isinstance(data, Decimal):
#         return float(data)  # or str(data) if you prefer to keep it as string
#     return data

# # Database Connection Setup
# def get_database_connection():
#     try:
#         connection = connect(**db_config)
#         return connection
#     except Error as e:
#         return f"Error connecting to database: {str(e)}"


# # Execute SQL Query
# def execute_sql_query(query):
#     connection = get_database_connection()
#     if isinstance(connection, str):  # Error message
#         return connection

#     try:
#         cursor = connection.cursor()
#         cursor.execute(query)
#         results = cursor.fetchall()

#         # Get column names
#         column_names = [desc[0] for desc in cursor.description]

#         cursor.close()

#         # Combine results with column names
#         return {
#             "columns": column_names,
#             "data": results
#         }
#     except Error as e:
#         return f"Error executing query: {str(e)}"
#     finally:
#         connection.close()


# # API and model configuration
# model_name = "gemini-1.5-pro"
# GEMINI_API_KEY = "AIzaSyC1YGJ7w9jy-UehVXK-G58R7hIqq2nmUdA"

# # Initialize the Google Gemini (Google GenAI) model
# chat_model = ChatGoogleGenerativeAI(
#     model=model_name,
#     google_api_key=GEMINI_API_KEY,
#     temperature=0,
#     convert_system_message_to_human=True
# )

# query_prompt = PromptTemplate(
#     input_variables=["user_input"],
#     template=(
#         "You are an AI that converts natural language into MySQL queries for filtering stocks. "
#         "Given the following columns and description of column  in the table 'StockDatanew' so you need to always use FROM stock_database.StockDatanew :\n"
#         "1. Stock_Name: The name of the listed company. Used to identify the organization behind the stock\n"
#         "2. NSEcode: Unique ticker code for the stock on the National Stock Exchange. Helps locate the stock quickly.\n"
#         "3. BSEcode: Unique ticker code for the stock on the Bombay Stock Exchange. Identifies the stock for trading on BSE.\n"
#         "4. ISIN: International Securities Identification Number assigned to each stock. Standardized globally for trading \n"
#         "5. Industry_Name: The sector or category the company operates in. Used for benchmarking and sector analysis\n"
#         "6. Current_Price: The most recent price at which the stock was traded. Indicates its current market valuation\n"
#         "7. Market_Capitalization_in_crores: The total market value of all outstanding shares of the company. Reflects company size\n"
#         "8. Trendlyne_Durability_Score: A score representing the company’s financial stability. Based on parameters like debt and earnings\n"
#         "9. Trendlyne_Valuation_Score: Score evaluating the stock’s relative valuation. Helps identify overvalued or undervalued stocks\n"
#         "10. Trendlyne_Momentum_Score: Score based on price momentum. Indicates whether the stock is gaining or losing value\n"
#         "11. DVM_classification_text: Classification of the stock’s durability, valuation, and momentum. Useful for holistic assessment.\n"
#         "12. Prev_Day_Trendlyne_Durability_Score: Stability score from the previous trading day. Used to track changes in financial health.\n"
#         "13. Prev_Day_Trendlyne_Valuation_Score: Stock valuation score from the previous trading day. Indicates short-term value trends.\n"
#         "14. Prev_Day_Trendlyne_Momentum_Score: Price momentum score from the previous day. Highlights daily momentum shifts.\n"
#         "15. Prev_Week_Trendlyne_Durability_Score: Durability score from the previous week. Useful for weekly trend analysis.\n"
#         "16. Prev_Week_Trendlyne_Valuation_Score: Valuation score from a week ago. Tracks changes in the stock’s value assessment\n"
#         "17. Prev_Week_Trendlyne_Momentum_Score: Momentum score from the previous week. Shows short-term price movement trends.\n"
#         "18. Prev_Month_Trendlyne_Durability_Score: Durability score as of the prior month. Evaluates stability over a longer horizon\n"
#         "19. Prev_Month_Trendlyne_Valuation_Score: Valuation score from a month ago. Compares current vs. past valuations.\n"
#         "20. Prev_Month_Trendlyne_Momentum_Score: Momentum score from the prior month. Useful for medium-term momentum tracking.\n"
#         "21. Normalized_Momentum_Score: Adjusted score measuring price momentum. Filters out market anomalies for clarity.\n"
#         "22. Operating_Revenue_Qtr: Total revenue generated during the quarter. Key indicator of business activity and scale.\n"
#         "23. Net_Profit_Qtr: Profit after all expenses during the quarter. Reflects company’s quarterly profitability.\n"
#         "24. Revenue_Growth_Qtr_YoY_Percent: Year-on-year percentage growth in quarterly revenue. Measures business growth rate\n"
#         "25. Net_Profit_Qtr_Growth_YoY_Percent: Year-on-year growth percentage in quarterly profits. Tracks profitability improvements\n"
#         "26. Sector_Revenue_Growth_Qtr_YoY_Percent: Revenue growth of the entire sector YoY. Benchmarks the company within its sector.\n"
#         "27. Sector_Net_Profit_Growth_Qtr_YoY_Percent: Sector-wide YoY net profit growth. Indicates industry-wide profit trends.\n"
#         "28. Sector_Revenue_Growth_Qtr_QoQ_Percent: Quarter-on-quarter revenue growth of the sector. Highlights seasonal variations.\n"
#         "29. Net_Profit_QoQ_Growth_Percent: Quarter-on-quarter profit growth. Useful for detecting recent profitability changes.\n"
#         "30. Sector_Net_Profit_Growth_Qtr_QoQ_Percent: Profit growth of the sector QoQ. Helps compare company vs. sector performance.\n"
#         "31. Operating_Profit_Margin_Qtr_Percent: The operating profit margin percentage for the last quarter. Indicates operational efficiency.\n"
#         "32. Operating_Profit_Margin_Qtr_1Yr_Ago_Percent: The operating profit margin percentage from the same quarter last year. For historical comparison.\n"
#         "33. Operating_Revenue_TTM: Trailing twelve-month revenue. Useful for assessing long-term financial performance.\n"
#         "34. Net_Profit_TTM: Trailing twelve-month net profit. Indicates long-term profitability trends.\n"
#         "35. Operating_Revenue_Annual: Revenue generated annually. Reflects the overall financial size of the business.\n"
#         "36. Net_Profit_Annual: Annual net profit achieved. Indicates company’s overall annual profitability\n"
#         "37. Revenue_Growth_Annual_YoY_Percent: Year-over-year annual revenue growth percentage. Shows yearly business growth.\n"
#         "38. Net_Profit_Annual_YoY_Growth_Percent: Annual net profit growth percentage year-over-year. Highlights long-term trends.\n"
#         "39  Sector_Revenue_Growth_Annual_YoY_Percent: Year-over-year annual revenue growth percentage for the sector. Provides sectoral context.\n"
#         "40. Cash_from_Financing_Annual_Activity: Cash generated or used in financing activities over the year. Reflects capital structure decisions. \n"
#         "41. Cash_from_Investing_Activity_Annual: Cash generated or used in investing activities annually. Indicates investment strategy. \n"
#         "42. Cash_from_Operating_Activity_Annual: Cash generated or used in operating activities annually. Shows operational cash flow. \n"
#         "43  Net_Cash_Flow_Annual: Net cash flow for the year. Represents overall liquidity and financial health\n"
#         "44  sector_name: The name of the industry sector to which the company belongs. Helps categorize and benchmark performance within a specific sector.\n"
#         "45  Latest_financial_result: Represents the most recent financial results reported by the company, such as quarterly or annual data. Reflects the latest performance metrics.\n"
#         "46  Result_Announced_Date: The date on which the company announced its latest financial results. Useful for tracking reporting timelines and market reactions\n"
#         "47  PE_TTM_Price_to_Earnings: The price-to-earnings ratio calculated based on trailing twelve months (TTM) earnings. Indicates how much investors are willing to pay per unit of earnings.\n"
#         "48  OneYr_Forward_Forecaster_Estimates_PE: The projected price-to-earnings ratio for the next year, based on forecaster estimates. Reflects expectations for future growth and profitability.\n"
#         "49  PE_3Yr_Average: The average price-to-earnings ratio over the last three years. Provides a historical perspective on valuation trends.\n"
#         "50  PE_5Yr_Average: The average price-to-earnings ratio over the past five years. Offers a longer-term view of valuation consistency\n"
#         "51. Percent_Days_Traded_Below_Current_PE_Price_to_Earnings: The percentage of trading days where the stock's PE ratio was below its current PE. Indicates the rarity or frequency of the current valuation level.\n"
#         "52. Sector_PE_TTM: The trailing twelve-month price-to-earnings ratio averaged across all companies in the sector. Helps compare the company's valuation to its peers.\n"
#         "53. Industry_PE_TTM: The trailing twelve-month price-to-earnings ratio averaged across companies in the industry. Provides a more granular comparison relative to specific competitors.\n"
#         "54. PEG_TTM_PE_to_Growth: The price-to-earnings-to-growth ratio based on TTM earnings. Combines valuation with growth to indicate how much investors are paying for future growth.\n"
#         "55. OneYr_Forward_Forecaster_Estimates_PEG: The projected PEG ratio for the next year, based on forecaster estimates. Reflects expectations of future valuation efficiency.\n"
#         "56. Sector_PEG_TTM: The average PEG ratio for the sector based on trailing twelve months. Indicates growth-adjusted valuations across the sector.\n"
#         "57. Industry_PEG_TTM: The average PEG ratio for the industry based on trailing twelve months. Provides a more specific growth-adjusted valuation benchmark.\n"
#         "58. Price_to_Book_Value: The ratio of the stock price to its book value per share. Indicates how the market values the company relative to its net asset value.\n"
#         "59. Percent_Days_Traded_Below_Current_Price_to_Book_Value: The percentage of trading days where the stock's price-to-book ratio was below its current level. Highlights how often the current valuation is exceeded\n"
#         "60. Sector_Price_to_Book_TTM: The trailing twelve-month price-to-book ratio averaged across all companies in the sector. Helps assess relative valuation within the sector.\n"
#         "61. Industry_Price_to_Book_TTM: The trailing twelve-month price-to-book ratio averaged across all companies in the industry. Provides an industry-specific valuation comparison.\n"
#         "62. Basic_EPS_TTM: The basic earnings per share over the trailing twelve months. Reflects the profitability allocated to each outstanding share.\n"
#         "63. EPS_TTM_Growth_Percent: The percentage growth in earnings per share over the trailing twelve months. Indicates improvement or decline in profitability.\n"
#         "64. ROE_Annual_Percent: The annual return on equity (ROE) expressed as a percentage. Measures profitability relative to shareholders' equity.\n"
#         "65. Sector_Return_on_Equity_ROE: The average annual return on equity for all companies in the sector. Helps benchmark the company’s performance within its sector.\n"
#         "66. Industry_Return_on_Equity_ROE: The average annual return on equity for all companies in the industry. Provides a narrower benchmark within specific industry peers.\n"
#         "67. RoA_Annual_Percent: The annual return on assets (ROA) expressed as a percentage. Reflects how efficiently the company uses its assets to generate profit.\n"
#         "68. Sector_Return_on_Assets: The average annual return on assets across all companies in the sector. A benchmark for operational efficiency within the sector\n"
#         "69. Industry_Return_on_Assets: The average annual return on assets across all companies in the industry. Indicates efficiency compared to direct competitors.\n"
#         "70. Piotroski_Score: A score based on nine financial criteria that measure a company’s financial strength and growth potential. Indicates the overall health of the company.\n"
#         "71. Day_MFI: The Money Flow Index for the day, calculated based on price and volume data. Used to measure buying and selling pressure.\n"
#         "72. Day_RSI: The Relative Strength Index for the day, indicating whether the stock is overbought or oversold on a scale of 0 to 100.\n"
#         "73. Day_MACD: The Moving Average Convergence Divergence for the day. Highlights the relationship between two moving averages of the stock's price.\n"
#         "74. Day_MACD_Signal_Line: The signal line for the MACD, used to generate buy or sell signals when it crosses the MACD line.\n"
#         "75. Day_SMA_30: The 30-day Simple Moving Average of the stock's price. Indicates the average closing price over the last 30 days.\n"
#         "76. Day_SMA_50: The 50-day Simple Moving Average of the stock's price. A mid-term trend indicator often used by traders.\n"
#         "77. Day_SMA_100: The 100-day Simple Moving Average of the stock's price. Represents a longer-term trend of the stock.\n"
#         "78. Day_SMA_200: The 200-day Simple Moving Average of the stock's price. A key indicator of long-term trends.\n"
#         "79. Day_SMA_5: The 5-day Simple Moving Average of the stock's price. Represents short-term price trends.\n"
#         "80. Day_EMA_12: The 12-day Exponential Moving Average of the stock's price. Gives more weight to recent prices for identifying trends.\n"
#         "81. Day_EMA_20: The 20-day Exponential Moving Average of the stock's price. Used to track short to medium-term trends.\n"
#         "82. Day_EMA_50: The 50-day Exponential Moving Average of the stock's price. Highlights mid-term momentum.\n"
#         "83. Day_EMA_100: The 100-day Exponential Moving Average of the stock's price. Focuses on long-term trend analysis.\n"
#         "84. Beta_1Month: The beta coefficient over the last one month, measuring the stock's volatility relative to the market.\n"
#         "85. Beta_3Month: The beta coefficient over the last three months. Reflects short-term market risk exposure.\n"
#         "86. Beta_1Year: The beta coefficient over the last one year. Indicates the stock's volatility relative to the broader market over the medium term.\n"
#         "87. Beta_3Year: The beta coefficient over the last three years. Captures long-term market risk trends for the stock.\n"
#         "88. Day_ROC21: The Rate of Change (ROC) over 21 days, measuring the percentage change in the stock's price over this period.\n"
#         "89. Day_ROC125: The Rate of Change (ROC) over 125 days, providing a long-term momentum indicator for the stock.\n"
#         "90. Day_ATR: The Average True Range for the day, showing the average volatility of the stock.\n"
#         "91. Day_ADX: The Average Directional Index for the day. Measures the strength of the stock's trend.\n"
#         "92. Pivot_Point: The pivot point calculated for the day, used to identify potential support and resistance levels.\n"
#         "93. First_Resistance_R1: The first level of resistance for a stock, indicating a price point where selling interest may emerge, potentially preventing further price increases.\n"
#         "94. First_Resistance_R1_to_Price_Diff_Percent: The percentage difference between the current price and the first resistance level, providing insight into the proximity of the price to this resistance.\n"
#         "95. Second_Resistance_R2: The second level of resistance, representing a higher price point where additional selling pressure may occur.\n"
#         "96. Second_Resistance_R2_to_Price_Diff_Percent: The percentage difference between the current price and the second resistance level, indicating the distance to this key price point\n"
#         "97. Third_Resistance_R3: The third level of resistance, a further price point that may present significant barriers to upward movement.\n"
#         "98. Third_Resistance_R3_to_Price_Diff_Percent: The percentage difference between the current price and the third resistance level, showing how far the price is from this level.\n"
#         "99. First_Support_S1: The first level of support for a stock, indicating a price point where buying interest may emerge, potentially preventing further price declines.\n"
#         "100. First_Support_S1_to_Price_Diff_Percent: The percentage difference between the current price and the first support level, highlighting the proximity to this support\n"
#         "101. Second_Support_S2: The second level of support, representing a deeper price point where additional buying pressure may occur.\n"
#         "102. Second_Support_S2_to_Price_Diff_Percent: The percentage difference between the current price and the second support level, indicating the distance to this critical price point.\n"
#         "103. Third_Support_S3: The third level of support, a further price point that may provide significant buying interest.\n"
#         "104. Third_Support_S3_to_Price_Diff_Percent: The percentage difference between the current price and the third support level, showing how far the price is from this support.\n"
#         "105. Day_Low: The lowest price of the stock during the current trading day.\n"
#         "106. Day_High: The highest price of the stock during the current trading day\n"
#         "107. Week_Low: The lowest price of the stock during the current week.\n"
#         "108. Week_High: The highest price of the stock during the current week.\n"
#         "109. Month_Low: The lowest price of the stock during the current month.\n"
#         "110. Month_High: The highest price of the stock during the current month\n"
#         "111. Qtr_Low: The lowest price of the stock during the current quarter.\n"
#         "112. Qtr_High: The highest price of the stock during the current quarter.\n"
#         "113. OneYr_Low: The lowest price of the stock over the past year.\n"
#         "114. OneYr_High: The highest price of the stock over the past year.\n"
#         "115. Day_Volume: The total trading volume of the stock for the current trading day, indicating the number of shares traded.\n"
#         "116. Week_Volume_Avg: The average trading volume of the stock over the current week, providing insight into typical trading activity\n"
#         "117. Month_Volume_Avg: The average trading volume of the stock over the current month, indicating broader trends in trading activity.\n"
#         "118. ThreeMonth_Volume_Avg: The average trading volume of the stock over the past three months, useful for assessing changes in interest and activity over time.\n"
#         "119. SixMonth_Volume_Avg: The average trading volume of the stock over the past six months, highlighting medium-term trends in trading volume.\n"
#         "120. Year_Volume_Avg: The average trading volume of the stock over the past year, reflecting long-term trading activity patterns.\n"
#         "121. Consolidated_End_of_Day_Volume: The total trading volume at the end of the trading day, combining all trading activity for that day.\n"
#         "122. Consolidated_Previous_End_of_Day_Volume: The total trading volume at the end of the previous trading day, useful for comparison with the current day’s volume.\n"
#         "123. Consolidated_5Day_Average_End_of_Day_Volume: The average end-of-day trading volume over the past five trading days, providing insight into recent trading trends.\n"
#         "124. Consolidated_30Day_Average_End_of_Day_Volume: The average end-of-day trading volume over the past 30 trading days, indicating the longer-term trading activity.\n"
#         "125. Consolidated_6M_Average_End_of_Day_Volume: The average end-of-day trading volume over the past six months, useful for assessing shifts in trading patterns.\n"
#         "126. Day_Volume_Multiple_of_Week: A metric showing how the current day's trading volume compares to the weekly average, indicating whether the day is experiencing unusually high or low activity.\n"
#         "127. vol_day_times_vol_week_strong: A measure indicating whether the current day's volume is significantly stronger than the weekly average, suggesting heightened interest or trading activity.\n"
#         "128. Consolidated_day_Volume: The total trading volume for the day across all exchanges or platforms, providing a comprehensive view of trading activity\n"
#         "129. VWAP_Day: The Volume-Weighted Average Price for the stock on the current trading day, representing the average price at which shares were traded, weighted by volume.\n"
#         "130. Promoter_holding_latest_percentage: The most recent percentage of shares held by promoters, indicating their stake in the company.\n"
#         "131. Promoter_holding_change_QoQ_percentage: The percentage change in promoter holdings from the previous quarter, reflecting shifts in promoter confidence or strategy.\n"
#         "132. Promoter_holding_change_4Qtr_percentage: The percentage change in promoter holdings over the past four quarters, useful for evaluating longer-term trends in promoter ownership.\n"
#         "133. Promoter_holding_change_8Qtr_percentage: The percentage change in promoter holdings over the past eight quarters, indicating more extended trends in promoter involvement.\n"
#         "134. Promoter_holding_pledge_percentage_Qtr: The percentage of promoter-held shares that are pledged as collateral for loans, reflecting potential financial risk\n"
#         "135. Promoter_pledge_change_QoQ_percent: The percentage change in the pledged promoter shares from the previous quarter, indicating changes in financial leverage or risk exposure.\n"
#         "136. MF_holding_current_Qtr_percentage: The percentage of shares held by mutual funds in the current quarter, indicating the level of institutional interest from mutual funds.\n"
#         "137. MF_holding_change_QoQ_percentage: The percentage change in mutual fund holdings from the previous quarter, reflecting trends in mutual fund investment activity.\n"
#         "138. MF_holding_change_1Month_percentage: The percentage change in mutual fund holdings over the past month, highlighting recent shifts in investment patterns.\n"
#         "139. MF_holding_change_2Month_percentage: The percentage change in mutual fund holdings over the past two months, providing insight into short-term trends in mutual fund investments.\n"
#         "140. MF_holding_change_3Month_percentage: The percentage change in mutual fund holdings over the past three months, indicating medium-term trends in mutual fund participation.\n"
#         "141. MF_holding_change_4Qtr_percentage: The percentage change in mutual fund holdings over the past four quarters, useful for assessing longer-term investment trends.\n"
#         "142. MF_holding_change_8Qtr_percentage: The percentage change in mutual fund holdings over the past eight quarters, indicating extended trends in mutual fund investments.\n"
#         "143. FII_holding_current_Qtr_percentage: The percentage of shares held by foreign institutional investors in the current quarter, reflecting international investment interest.\n"
#         "144. FII_holding_change_QoQ_percentage: The percentage change in FII holdings from the previous quarter, indicating shifts in foreign institutional investment behavior.\n"
#         "145. FII_holding_change_4Qtr_percentage: The percentage change in FII holdings over the past four quarters, providing insights into long-term trends in foreign investment.\n"
#         "146. FII_holding_change_8Qtr_percentage: The percentage change in FII holdings over the past eight quarters, indicating extended trends in foreign institutional investment.\n"
#         "147. Institutional_holding_current_Qtr_percentage: The total percentage of shares held by all institutional investors in the current quarter, indicating overall institutional interest.\n"
#         "148. Institutional_holding_change_QoQ_percentage: The percentage change in institutional holdings from the previous quarter, reflecting changes in institutional investment activity.\n"
#         "149. Institutional_holding_change_4Qtr_percentage: The percentage change in institutional holdings over the past four quarters, useful for assessing longer-term institutional trends.\n"
#         "150. Institutional_holding_change_8Qtr_percentage: The percentage change in institutional holdings over the past eight quarters, indicating extended trends in institutional ownership.\n"
#         "Important guidelines:\n"
#         "1. Always include the 'stock_database.StockDatanew' table in the query.\n"
#         "2. Ensure the query is compatible with MySQL's 'ONLY_FULL_GROUP_BY' mode by:\n"
#         "   - Including all non-aggregated columns in the GROUP BY clause.\n"
#         "   - Using aggregate functions like MAX, MIN, AVG, SUM for columns not included in GROUP BY.\n"
#         "3. If the query involves retrieving specific rows (e.g., the row corresponding to the maximum or minimum value of a column):\n"
#         "   - Use subqueries to find the maximum or minimum value and filter rows accordingly.\n"
#         "   - Alternatively, use window functions (if supported) to rank rows and filter the top-ranked ones.\n"
#         "4. For ranking or retrieving the top results within groups, prefer window functions such as RANK() or ROW_NUMBER() "
#         "in MySQL 8.0+.\n"
#         "5. For selecting columns like 'Stock_Name' along with aggregated values, ensure the query logic includes either a subquery or "
#         "window function to avoid conflicts with ONLY_FULL_GROUP_BY.\n"
#         "6. Avoid common SQL syntax issues and ensure all column names, conditions, and clauses are valid for MySQL.\n\n"

#         "Transform the following user input into a valid SQL query:\n\n"
#         "User Input: {user_input}\n\n"
#         "Output only the SQL query without any additional text, including the database name for example:- 'SELECT Stock FROM stock_data.stocks ORDER BY MarketCap DESC'\n"
#     )
# )

# chain = LLMChain(llm=chat_model, prompt=query_prompt)

# # Function to Generate and Execute SQL Query
# # Function to Generate and Execute SQL Query
# def chat_to_query(user_input):
#     try:
#         # Convert user input to SQL query
#         sql_query = chain.run(user_input)
#         sql_query = sql_query.replace("```sql\n", "").replace("```", "").strip()
#         print(f"\nGenerated SQL Query:\n{sql_query}")

#         # Execute the SQL query
#         results = execute_sql_query(sql_query)
#         if isinstance(results, dict):
#             # Convert Decimal types to float
#             results['data'] = [convert_to_float(row) for row in results['data']]
#             # return json.dumps(results, indent=4)
#             return results
#         else:
#             return json.dumps({"error": results}, indent=4)
#     except Exception as e:
#         return json.dumps({"error": str(e)}, indent=4)


# # Main Function
# def response_q(qus):
#     # user_input = "top 10 stocks having highest marketcap"
#     user_input = qus
#     try:
#         results = chat_to_query(user_input)
#         return  results
#     except Exception as e:
#         return str(e)
 



