# from chat_data_fetcher import run_query
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

from mysql.connector import connect, Error
from decimal import Decimal
from django.db import connection



def execute_sql_query(query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params) 
            if query.strip().lower().startswith("select"):
                results = cursor.fetchall()
            else:
                connection.commit()
                results = f"Query executed successfully: {cursor.rowcount} rows affected."
        cursor.close()
        return results
    except Exception as e:
        return f"Error executing query: {str(e)}"


# Function to Generate and Execute SQL Query
def run_query(sql_query, params=None):
    try:
        results = execute_sql_query(sql_query, params)
        if isinstance(results, list):  # Check if results are valid rows
            # Convert Decimal objects to float where applicable
            processed_results = [
                [float(item) if isinstance(item, (int, float, Decimal)) else item for item in row]
                for row in results
            ]
            return processed_results
        return results  # Error message or other output
    except Exception as e:
        return f"Error: {str(e)}"

def fundamental_analysis(ticke):
    ticker = ticke

    sample_query = '''
        SELECT
            stock_name,
            sector_name,
            pe_ttm_price_to_earnings,
            sector_pe_ttm,
            basic_eps_ttm,
            operating_profit_margin_qtr_percent,
            (operating_revenue_ttm / market_capitalization_in_crores) AS Cash_flow_yield
        FROM
            stockdata
        WHERE
            ISIN = %s;
        '''
    parm = (ticker,)  # Tuple for parameterized query
    response = run_query(sample_query, parm)

    if isinstance(response, list) and len(response) > 0:
        company_symbol, sector, pe_ratio, sector_pe_ratio, eps, operating_margin, cash_flow_yield = response[0]
        #print(response)

        sample_query1 = '''
            SELECT
                AVG(operating_profit_margin_qtr_percent),
                AVG(operating_revenue_ttm / market_capitalization_in_crores) AS sector_cash_flow
            FROM
                stockdata
            WHERE
                sector_name = %s;
            '''
        response1 = run_query(sample_query1, (sector,))
        competitors_operating_margin, sector_cash_flow_yield = response1[0]
        #print(response1)

    else:
        print("No data returned or error:", response)

    def create_prompt(company_symbol, pe_ratio, sector_pe_ratio, eps, operating_margin,
                      competitors_operating_margin, cash_flow_yield, sector_cash_flow_yield):
        prompt = f"""
        I need a fundamental analysis of {company_symbol} based on key financial metrics.

        *Valuation Metrics:*
        - Sector P/E Ratio: {sector_pe_ratio}
        - Current Stock P/E Ratio: {pe_ratio}

        *Valuation Analysis:*
        The stock's P/E ratio of {pe_ratio} is {('overvalued' if pe_ratio > sector_pe_ratio else 'undervalued')} compared to the sector average of {sector_pe_ratio}.

        *Earnings Quality:*
        - EPS: {eps}
        - Operating Margin: {operating_margin}%

        *Earnings Analysis:*
        With an EPS of {eps} and an operating margin of {operating_margin}%, the company {('outperforms' if operating_margin > competitors_operating_margin else 'underperforms')} its competitors.

        *Cash Flow:*
        - Cash Flow Yield: {cash_flow_yield}%
        - Sector Cash Flow Yield: {sector_cash_flow_yield}%

        *Cash Flow Analysis:*
        A cash flow yield of {cash_flow_yield}% indicates {('strong' if cash_flow_yield > sector_cash_flow_yield else 'weaker')} cash generation compared to the sector average of {sector_cash_flow_yield}%.

        *Overall Analysis:*
        Summarize the company’s overall financial health based on the provided parameters and give an investment outlook considering growth, stability, or risks.

        Example Output:

        Valuation:
        "At a P/E of {pe_ratio}, the stock is {('at a premium' if pe_ratio > sector_pe_ratio else 'at a discount')} to {sector_pe_ratio}, suggesting investors {('expect higher growth' if pe_ratio > sector_pe_ratio else 'expect lower growth')}."

        Earnings:
        "With an EPS of {eps} and a margin of {operating_margin}%, the company is {('outperforming' if operating_margin > competitors_operating_margin else 'underperforming')} competitors with a margin of {competitors_operating_margin}%. The margin has (change details can be added), indicating improved/increasing costs."

        Cash Flow:
        "The cash flow yield of {cash_flow_yield}% is {('better' if cash_flow_yield > sector_cash_flow_yield else 'worse')} than {sector_cash_flow_yield}%, indicating {('strong' if cash_flow_yield > sector_cash_flow_yield else 'concerns about cash generation')}."

        Overall:
        "The financial metrics suggest the company is {('well-positioned' if operating_margin > competitors_operating_margin else 'risk-prone')} in valuation, profitability and cash flow generation."
        """

        return prompt
    prompt = create_prompt(
        company_symbol=company_symbol,
        pe_ratio=pe_ratio,
        sector_pe_ratio=sector_pe_ratio,
        eps=eps,
        operating_margin=operating_margin,
        competitors_operating_margin=competitors_operating_margin,
        cash_flow_yield=cash_flow_yield,
        sector_cash_flow_yield=sector_cash_flow_yield,
    )
    return prompt

def technical_analysis(ticker):
    sample_query = '''
        SELECT
            stock_name,
            sector_name,
            Current_Price,
            Day_RSI,
            Day_MACD,
            Day_MACD_Signal_Line
        FROM
            stockdata
        WHERE
            ISIN = %s;
        '''
    parm = (ticker,)  # Tuple for parameterized query
    response = run_query(sample_query, parm)

    if isinstance(response, list) and len(response) > 0:
        company_symbol, sector, close_price, rsi, macd_value, macd_signal = response[0]
        #print(response)
    else:
        print("No data returned or error:", response)

    prompt = f"""
*Technical Analysis for {ticker}:*

1. *Current Price*:
   - The stock is currently trading at ₹{close_price:.2f}.


2. *Relative Strength Index (RSI)*:
   - RSI: {rsi:.2f}.
   - Status: {'Overbought (above 70)' if rsi > 70 else 'Neutral (30-70)' if 30 <= rsi <= 70 else 'Oversold (below 30)'}.
   - Interpretation: {'The RSI suggests overbought conditions, which may lead to a pullback.' if rsi > 70 else 'The RSI is in a neutral zone, showing no strong trend signal.' if 30 <= rsi <= 70 else 'The RSI indicates oversold conditions, which may signal undervaluation or potential rebound.'}

3. *MACD (Moving Average Convergence Divergence)*:
   - MACD Value: {macd_value:.2f}.
   - Signal Line: {macd_signal:.2f}.
   - Status: {'Bullish: MACD is above the signal line, suggesting upward momentum.' if macd_value > macd_signal else 'Bearish: MACD is below the signal line, indicating downward momentum.'}
   - Crossover: {'The MACD recently crossed above the signal line, signaling potential bullish momentum.' if macd_value > macd_signal else 'The MACD recently crossed below the signal line, signaling potential bearish momentum.'}
"""

    return prompt
def growth_performance(ticke):
    sample_query = '''
                SELECT
                    stock_name,
                    sector_name,
                    operating_revenue_ttm,
                    ROE_Annual_Percent,
                    RoA_Annual_Percent
                FROM
                    stockdata
                WHERE
                    ISIN = %s;
                '''
    parm = (ticke,)  # Tuple for parameterized query
    response = run_query(sample_query, parm)

    if isinstance(response, list) and len(response) > 0:
        ticker, sector, revenue_current_year, roe, roa = response[0]
        print(response)

        sample_query1 = '''
                    SELECT
                        AVG(ROE_Annual_Percent),
                        AVG(RoA_Annual_Percent)
                    FROM
                        stockdata
                    WHERE
                        sector_name = %s;
                    '''
        response1 = run_query(sample_query1, (sector,))
        sector_roe, sector_roa = response1[0]
        print(response1)

    else:
        print("No data returned or error:", response)

    analysis_prompt = f"""
        As a financial AI advisor, I want you to analyze the Growth Prospects and Profitability of {ticker} based on the following data:

        ### Growth Prospects:

        1. *Revenue Growth:*
           - Revenue of the stock: ₹{revenue_current_year:,.2f}
           - Revenue growth of the sector competitor  {sector_roe:.2f}%

        ### Profitability:

        1. *Return on Equity (ROE):*
           - ROE of the stock: {roe:.2f}%
           - ROE of the sector competitor  {sector_roe:.2f}%

           ROE is currently at {roe:.2f}%, above the sector average of {sector_roe:.2f}%. This indicates that the stock is generating higher returns on shareholder equity compared to its competitors.

        2. *Return on Assets (ROA):*
           - ROA of the stock: {roa:.2f}%
           - ROA of the sector competitor  {sector_roa:.2f}%

           With an ROA of {roa:.2f}%, compared to the sector average of {sector_roa:.2f}%, the company shows efficient use of its assets, which is a positive indicator of its profitability.
        """

    # Print the final analysis prompt
    return analysis_prompt

def stock_performance(stock_ticker):
    def fetch_stock_data(stock_ticker):
        # Fetch stock data using yfinance
        stock = yf.Ticker(stock_ticker)

        # Get today's date and dates for 30 days ago and 180 days ago
        today = datetime.today().strftime('%Y-%m-%d')
        thirty_days_ago = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        one_eighty_days_ago = (datetime.today() - timedelta(days=180)).strftime('%Y-%m-%d')

        # Download historical stock data
        data = stock.history(start=one_eighty_days_ago, end=today)

        # Get the current price, 30 days ago price, and 180 days ago price
        current_price = data['Close'][-1]
        price_30_days_ago = data.loc[data.index == thirty_days_ago]['Close']
        price_180_days_ago = data.loc[data.index == one_eighty_days_ago]['Close']

        # If no exact date match is found for 30 days ago or 180 days ago, use nearest date
        if price_30_days_ago.empty:
            price_30_days_ago = data['Close'][-22]  # Approximation of 30 trading days
        else:
            price_30_days_ago = price_30_days_ago[0]

        if price_180_days_ago.empty:
            price_180_days_ago = data['Close'][0]  # Earliest available data (180 days ago)
        else:
            price_180_days_ago = price_180_days_ago[0]

        return current_price, price_30_days_ago, price_180_days_ago

    def generate_stock_prompt(stock_name, current_price, price_30_days_ago, price_180_days_ago):
        # Calculate percentage changes
        short_term_change = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
        long_term_change = ((current_price - price_180_days_ago) / price_180_days_ago) * 100

        # Generate the analysis prompt
        analysis_prompt = f"""
        As a financial AI advisor, analyze the stock's current performance and trends using the following details:

        Current Price: ${current_price:.2f}
        Price 30 days ago: ${price_30_days_ago:.2f}
        Price 180 days ago: ${price_180_days_ago:.2f}

        Based on this information, provide a Stock Performance Overview. The output should look something like this:
        "{stock_name} stock is currently valued at ${current_price:.2f}, {'up' if short_term_change > 0 else 'down'} {abs(short_term_change):.2f}% over the last 30 days. The {'increase' if long_term_change > 0 else 'decrease'} in valuation is supported by a long-term trend over the last 6 months, during which the stock has {'increased' if long_term_change > 0 else 'decreased'} by {abs(long_term_change):.2f}% from ${price_180_days_ago:.2f} to ${current_price:.2f}."
        """

        return analysis_prompt

    current_price, price_30_days_ago, price_180_days_ago = fetch_stock_data(stock_ticker)
    prompt = generate_stock_prompt(stock_ticker, current_price, price_30_days_ago, price_180_days_ago)
    return prompt


