import urllib.parse
import certifi
import logging
from pymongo import MongoClient
from mysql.connector import connect, Error
from decimal import Decimal
import pyodbc
from datetime import datetime
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from tool_helper_mysql import fundamental_analysis, technical_analysis
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# API and model configuration
model_name = "gemini-1.5-pro"
GEMINI_API_KEY = ""

# Initialize the Google Gemini (Google GenAI) model
chat_model = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    convert_system_message_to_human=True
)

query_prompt = PromptTemplate(
    input_variables=["user_input"],
    template=(
        "You are a highly sophisticated financial analyst bot designed to assist users with in-depth financial insights. "
        "Based on the following user input:\n\n{user_input}\n\n"
        "Provide a detailed, professional, and actionable financial analysis."
    )
)
chain = LLMChain(llm=chat_model, prompt=query_prompt)

query_prompt = PromptTemplate(
    input_variables=["user_input"],
    template=(
        "You are a highly sophisticated financial analyst bot designed to assist users with in-depth financial insights. "
        "Based on the following user input:\n\n{user_input}\n\n"
        "Provide a detailed, professional, and actionable financial analysis."
    )
)
chain = LLMChain(llm=chat_model, prompt=query_prompt)

# MongoDB credentials
username = urllib.parse.quote_plus("")
password = urllib.parse.quote_plus("")
ca = certifi.where()

# Initialize MongoDB connection
logging.basicConfig(level=logging.INFO)
logging.info("Connecting to MongoDB Atlas...")
try:
    client = MongoClient(f"mongodb+srv://{username}:{password}@mongo1.i4fu33h.mongodb.net/?retryWrites=true&w=majority",
                         tlsCAFile=ca)
    db = client['stock_news_db']  # Database name
    article_collection = db['news_articles']  # Collection for storing articles
    logging.info("MongoDB connection established.")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise


# Function to fetch news articles for a specific company
def fetch_news(company_name):
    """Fetch news articles related to the specified company name."""
    try:
        # Query the collection for articles containing the company name
        articles = article_collection.find(
            {"company": {"$regex": company_name, "$options": "i"}}  # Adjust field as needed
        )
        articles_list = list(articles)

        if articles_list:
            logging.info(f"Found {len(articles_list)} articles for {company_name}.")
            return articles_list
        else:
            logging.info(f"No articles found for {company_name}.")
            return []
    except Exception as e:
        logging.error(f"Failed to fetch articles: {e}")
        return []


def calculate_average_sentiment(articles):
    """Calculate the average sentiment from a list of articles."""
    if not articles:
        return 0.0  # Return 0 if there are no articles

    total_sentiment = sum(article.get('sentiment', 0) for article in articles)
    average_sentiment = total_sentiment / len(articles)
    return average_sentiment



# Database Configuration
db_config = {
    'host': 'mysqlserver1235.mysql.database.azure.com',
    'database': 'stock_database',
    'user': '',
    'password': '',
    'ssl_ca': r"C:\Users\Abhishek Saraswat\Downloads\DigiCertGlobalRootG2.crt.pem"
}

db_config1 = {
    'server': 'stockdatabase123.database.windows.net',
    '
}
def get_db_connection():
    try:
        conn_str = (
            f"DRIVER={db_config1['driver']};"
            f"SERVER={db_config1['server']};"
            f"PORT=1433;"
            f"DATABASE={db_config1['database']};"
            f"UID={db_config1['username']};"
            f"PWD={db_config1['password']}"
        )
        connection = pyodbc.connect(conn_str)
        logging.info("Successfully connected to the azure database.")
        return connection
    except Exception as e:
        logging.error("Failed to connect to the azure database.", exc_info=True)
        raise


def fetch_data_from_azure(cursor):
    sql_query = f"""SELECT Day_chaange_percent FROM dbo.IndicieDatas  WHERE Indicie_name ="Nifty 50" """  # Updated table name
    try:
        cursor.execute(sql_query)
        logging.info(f"Nifty 50 Data fetched.")
    except Exception as e:
        logging.error(f"Failed to fetch Nifty 50 Data.", exc_info=True)
        raise


# Main function
def fetching_data_azure():
    connection = None
    data = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # fetch row from azure database
        data = fetch_data_from_azure(cursor)

        connection.commit()
        logging.info("Data fetched successfully.")
    except Exception as e:
        logging.error("An error occurred during processing.", exc_info=True)
        if connection:
            connection.rollback()  # Rollback changes on error
    finally:
        if connection:
            connection.close()
            logging.info("Database connection closed.")
    return data

# Weights for different durations
weights_by_duration = {
    "short_term": {"wD": 0.2, "wV": 0.2, "wM": 0.6},  # Short-term: 1–90 days
    "medium_term": {"wD": 0.35, "wV": 0.35, "wM": 0.3},  # Medium-term: 91–180 days
    "long_term": {"wD": 0.5, "wV": 0.3, "wM": 0.2},  # Long-term: 181–360 days
}


# Recommendation based on adjusted score
def recommend_stock(adjusted_score):
    if adjusted_score > 80:
        return "Strong Buy"
    elif 65 <= adjusted_score <= 80:
        return "Buy"
    elif 50 <= adjusted_score < 65:
        return "Hold"
    elif 30 <= adjusted_score < 50:
        return "Sell"
    else:
        return "Strong Sell"


# Calculate adjusted score
def calculate_adjusted_score(durability, valuation, momentum, weights):
    """
    Calculate the adjusted score for stock recommendation.
    Converts inputs to float to handle decimal.Decimal values.
    """
    # Convert inputs to float if necessary
    durability = float(durability) if isinstance(durability, Decimal) else durability
    valuation = float(valuation) if isinstance(valuation, Decimal) else valuation
    momentum = float(momentum) if isinstance(momentum, Decimal) else momentum

    adjusted_score = (
            weights["wD"] * durability +
            weights["wV"] * valuation +
            weights["wM"] * momentum
    )
    return adjusted_score


# Process stock data from the database
def process_stock_data(companies):
    # List of valid companies
      # Add more companies as needed
    try:
        # Connect to the database
        with connect(**db_config) as connection:
            query1 = "SELECT Stock_Name, Trendlyne_Durability_Score, Trendlyne_Valuation_Score, ISIN,Trendlyne_Momentum_Score, Current_Price, sector_name FROM StockDatanew"
            query2 = """
                    SELECT StockName AS Stock_Name, AverageRating, AverageTargetPrice, 
                           EcartObjDr, NbrOfAnalysts 
                    FROM Analyst_database
                """
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query1)
                rows1= cursor.fetchall()
                cursor.execute(query2)
                rows2 = cursor.fetchall()
                # Convert rows2 into a dictionary for quick lookup
                analyst_data = {row['Stock_Name']: row for row in rows2}
                #print(analyst_data)

                # Process and display stocks
                print("Stocks with 'Buy' or 'Strong Buy' recommendation for Short-Term Duration:")
                print("=" * 80)

                for row in rows1:
                    stock_name = row['Stock_Name']
                    durability_score = float(row['Trendlyne_Durability_Score'])
                    valuation_score = float(row['Trendlyne_Valuation_Score'])
                    momentum_score = float(row['Trendlyne_Momentum_Score'])
                    current_price = float(row['Current_Price'])
                    sector_name = str(row['sector_name'])
                    ISIN = str(row['ISIN'])



                    # Calculate short-term adjusted score
                    short_term_weights = weights_by_duration["short_term"]
                    adjusted_score = calculate_adjusted_score(
                        durability_score, valuation_score, momentum_score, short_term_weights
                    )
                    recommendation = recommend_stock(adjusted_score)

                    # Filter and print only "Buy" or "Strong Buy" recommendations
                    if stock_name in companies:
                        print(f"Stock: {stock_name}")
                        print(f"Sector: {sector_name}")
                        print(f"Current Price: {current_price}")
                        print(f"Adjusted Score: {adjusted_score:.2f}")
                        print(f"Recommendation: {recommendation}")
                        # Generate output using the model
                        print("Fundamental Analysis")
                        user_input = fundamental_analysis(str(ISIN))
                        response = chain.run(user_input)
                        # Function to process a single company's fundamental analysis
                        print(response)

                        print("Technical Analysis")

                        user_input = technical_analysis(str(ISIN))
                        response = chain.run(user_input)
                        # Function to process a single company's fundamental analysis
                        print(response)


                        # Check if stock exists in analyst data and print additional details
                        if stock_name in analyst_data:
                            analyst = analyst_data[stock_name]
                            if analyst:
                                average_rating = analyst['AverageRating']
                                average_target_price = analyst['AverageTargetPrice']
                                number_of_analysts = analyst['NbrOfAnalysts']
                                print(
                                    f"{stock_name} has {number_of_analysts} recommendations from analysts for a target price of {average_target_price} with a consensus level of {average_rating}.")

                        print("-" * 40)

    except Error as e:
        print(f"Error: {e}")

def fetch_todays_data():
    try:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        todays_data = article_collection.find({"date": {"$gte": today}})
        results = list(todays_data)
        logging.info(f"Fetched {len(results)} documents for today's date.")
        return results
    except Exception as e:
        logging.error(f"Error while fetching today's data: {e}")
        return []


def fetch_nifty50_data():
    try:
        # Connect to the database
        with connect(**db_config) as connection:
            query = """
                SELECT Indicie_name, Day_change_percent, LTP 
                FROM IndicieDatas
                WHERE Indicie_name = 'Nifty 50'  -- Filter for Nifty 50
            """
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                # Print the results for Nifty 50
                print("Nifty 50 Data:")
                print("=" * 40)
                if rows:
                    for row in rows:
                        indicie_name = row['Indicie_name']
                        day_change_percent = row['Day_change_percent']
                        ltp = row['LTP']
                        print(f"Indicie Name: {indicie_name}, Day Change (%): {day_change_percent}, LTP: {ltp}")
                else:
                    print("No data found for Nifty 50.")

    except Error as e:
        print(f"Error: {e}")


def fetch_stock_sectors(stock_list):
    stock_sector_list = []

    # Establishing the connection to the database
    with connect(**db_config) as connection:
        cursor = connection.cursor()

        # Create a placeholder string for the stock names
        placeholders = ', '.join(['%s'] * len(stock_list))
        query = f"SELECT Stock_Name, sector_name FROM StockDatanew WHERE Stock_Name IN ({placeholders})"

        # Execute the query with the stock list as parameters
        cursor.execute(query, stock_list)

        # Fetch all rows
        results = cursor.fetchall()

        # Creating a list of tuples (Stock_Name, sector_name)
        stock_sector_list = [(row[0], row[1]) for row in results]

    return stock_sector_list


def fetch_sector_day_change_by_list(sector_list):
    """
    Fetch day change percentages for a given list of sectors from the sector_data table.

    Args:
        db_config (dict): Database configuration dictionary.
        sector_list (list): List of sector names.

    Returns:
        list: A list of tuples containing sector names and their day change percentages.
    """
    sector_day_change_list = []

    # Establishing the connection to the database
    with connect(**db_config) as connection:
        cursor = connection.cursor()

        # Create a placeholder string for the sector names
        placeholders = ', '.join(['%s'] * len(sector_list))
        query = f"SELECT sector_name, Day_Change_Percent FROM sector_data WHERE sector_name IN ({placeholders})"

        # Execute the query with the sector list as parameters
        cursor.execute(query, sector_list)

        # Fetch all rows
        results = cursor.fetchall()

        # Creating a list of tuples (sector_name, Day_Change_Percent)
        sector_day_change_list = [(row[0], row[1]) for row in results]

    return sector_day_change_list


fetch_nifty50_data()
#print(fetching_data_azure())
# Example usage
companies = ['20 Microns Ltd.', '360 One Wam Ltd.', '3M India Ltd.']  # Replace with the desired company names

# Fetch sectors for the given companies
stock_sectors = fetch_stock_sectors( companies)

# Extract sector names from the fetched stock sectors
sector_names = [sector for stock, sector in stock_sectors]  # This will create a list of sector names

# Fetch day change percentages for the extracted sector names
sector_day_changes = fetch_sector_day_change_by_list( sector_names)

# Print the sector and its corresponding day change percentage
for sector, day_change in sector_day_changes:
    print(f"Sector: {sector}, Day Change Percent: {day_change:.2f}%")

    for company in companies:
        articles = fetch_news(company)
        average_sentiment = calculate_average_sentiment(articles)

        print(f"\nCompany: {company}, Average Sentiment: {average_sentiment:.2f}")

        # Print news articles for the company
        if articles:
            print("News Articles:")
            for article in articles:
                title = article.get('title', 'No Title')
                link = article.get('link', 'No Link')
                snippet = article.get('snippet', 'No Snippet')
                print(f"- Title: {title}\n  Link: {link}\n  Snippet: {snippet}\n")
        else:
            print("No news articles found.")

process_stock_data(companies)
data = fetch_todays_data()
for entry in data:
    print(entry)


