from django.test import TestCase

# Create your tests here.
# def gen_ai_response(question):
#     prompt =f""" 
#     This is question asked by user:{question}./n
#     Provide detailed information about use question, if it is related to stock including its current price, historical performance (1 month, 6 months, 1 year), market capitalization, P/E ratio, dividend yield, key financials, recent news, and analyst recommendations. Highlight any significant trends or news that might impact its future performance
#     return the response in markdown format
#     """
#     genai.configure(api_key=os.getenv("GENAI_API_KEY"))
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(question)
#     # markdown2.markdown(response.text)
#     return response.text