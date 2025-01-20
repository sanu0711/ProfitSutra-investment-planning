from langchain.agents import AgentType, initialize_agent
from langchain_community.utilities import SearchApiAPIWrapper
from langchain_core.tools import Tool
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
import yfinance as yf
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from .analysis_helper import growth_performance, technical_analysis, fundamental_analysis,stock_performance
import warnings
from dotenv import load_dotenv
import os
load_dotenv()

warnings.filterwarnings("ignore")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

model_name = "gemini-1.5-flash-8b"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    convert_system_message_to_human=True
)

# Define the tools for stock performance and financial analysis
@tool("Stock Performance")
def stock_performance_analysis(symbol: str) -> str:
    """Stock Performance analysis tool that takes a stock ticker as input and generates a prompt for a detailed Stock Performance analysis.for example 'TCS.NS','RELIANCE.NS'   """
    return stock_performance(symbol)


@tool("Growth Prospects and Profitability")
def growth_analysis(symbol: str) -> str:
    """Growth Prospects and Profitability analysis tool that takes a stock ISIN as input and generates a prompt for a detailed Growth Prospects and Profitability analysis. For example, you can use 'INE467B01029' (TCS) or 'INE002A01018' (Reliance) to analyze Tata Consultancy Services or Reliance Industries, respectively.  """
    return growth_performance(symbol)

@tool("Technical Analysis")
def technical(symbol: str) -> str:
    """Technical analysis tool that takes a stock ISIN as input and generates a prompt for a detailed technical analysis. For example, 'INE467B01029' (TCS), 'INE002A01018' (Reliance).  """
    return technical_analysis(symbol)

@tool("Fundamental Analysis")
def fundamental(symbol: str) -> str:
    """This tool performs fundamental analysis on a company based on its stock ISIN. It requires an ISIN that is compatible with financial data sources. For example, you can use 'INE467B01029' (TCS), 'INE002A01018' (Reliance Industries), or 'INE584A01023' (NMDC) to analyze Tata Consultancy Services, Reliance Industries, or NMDC, respectively."""
    return fundamental_analysis(symbol)

@tool("Brave-Search-Tool")
def brave_search(query: str) -> str:
    """A search engine. Useful for when you need news or to answer questions about current events. Input should be a search query."""
    duck = DuckDuckGoSearchRun()
    return duck.invoke(query)

@tool("Trading_Research")
def researcher(query: str) -> str:
    """Useful for when you need to find financial news about a public company. Input should be a company ticker. For example, AAPL for Apple, MSFT for Microsoft."""
    Yfinance = YahooFinanceNewsTool()
    return Yfinance.run(query)

def run_agent(input_text):
    prompt = PromptTemplate(
    input_variables=["chat_history", "input_text"],
    template=(
        "You are an AI financial assistant. Analyze the stock based on user input.\n"
        "Previous conversations:\n{chat_history}\n"
        "Current question: {input_text}\n"
        "Answer in a detailed yet concise manner."
        "Provide the output in html code Use appropriate headers, lists, tables, code blocks, or other tag elements as needed and for design use bootstrap 5 classes.\n"
        "ignore including cdn library, return only raw content inside div container id=raw-content.\n"
        "this output directly served in the chatbot interface so design accordingly.\n"
        
        )
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = initialize_agent(
    tools=[brave_search, fundamental,  technical, growth_analysis],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=False,
    memory=memory
    )
    result = agent.run(input_text)
    chat_history = memory.load_memory_variables({})["chat_history"]

    if len(chat_history) > 1:
        last_two_messages = chat_history[-2:]
    else:
        last_two_messages = chat_history

    formatted_chat_history = "\n".join(
        [f"User: {msg.content}" if msg.type == "human" else f"AI: {msg.content}" for msg in last_two_messages]
    )

    result = llm_chain.run({"chat_history": formatted_chat_history, "input_text": input_text})

    return result