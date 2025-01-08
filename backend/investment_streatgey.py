from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# API and model configuration
model_name = "gemini-1.5-pro"
GEMINI_API_KEY = "AIzaSyC1YGJ7w9jy-UehVXK-G58R7hIqq2nmUdA"

# Initialize the Google Gemini (Google GenAI) model
chat_model = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

investment_planning_prompt = PromptTemplate(
    input_variables=[
        "monthly_net_income", "other_income_sources", "age", "marital_status",
        "dependents", "housing", "utilities", "transport", "insurance",
        "loan_payments", "subscriptions", "college_debts", "groceries",
        "dining_out", "entertainment", "personal_care", "travel",
        "miscellaneous", "outstanding_debt", "interest_rates",
        "loan_tenure", "prioritization", "career_changes", "major_purchases",
        "life_events", "percent", "yes_no", "investment_risk"
    ],
    template="""
You are an investment planner assistant. Based on the user's financial details, provide a comprehensive expense management plan and investment strategy. 

### User Data:
1. **Monthly Net Income(after taxation):** {monthly_net_income}
2. **Other Income Sources:** {other_income_sources}
3. **Age:** {age}
4. **Marital Status:** {marital_status}
5. **Number of Dependents:** {dependents}

### Fixed Monthly Expenses:
- Housing Costs: {housing}
- Utilities: {utilities}
- Transport: {transport}
- Insurance: {insurance}
- Loan Payments: {loan_payments}
- Subscriptions: {subscriptions}
- College Debts: {college_debts}

### Variable Monthly Expenses:
- Groceries: {groceries}
- Dining Out: {dining_out}
- Entertainment: {entertainment}
- Personal Care: {personal_care}
- Travel: {travel}
- Miscellaneous: {miscellaneous}

### Debts and Loans:
- Outstanding Debt: {outstanding_debt}
- Interest Rates: {interest_rates}
- Loan Tenure: {loan_tenure}

### Savings and Investment Goals:
- Prioritization: {prioritization}

### Expected Future Changes:
- Career Changes: {career_changes}
- Major Purchases: {major_purchases}
- Life Events: {life_events}

### Preferences:
- Percentage of income to allocate to savings and investments: {percent}
- Comfortable in making lifestyle adjustments to increase savings: {yes_no}
- Investment risk: {investment_risk}

Compare the spending with the benchmark stated in the appendix, provide suggestions to user as to how they can decrease their expenses. 

Appendix

In the tables below we have shared data for Salaried employees for 25 -30 years of age, unmarried 

1. Up to ₹6 LPA (₹0 - ₹50,000 per month)
Category
Percentage
Amount (₹)
Description
Housing (Rent)
20-25%
₹10,000 - ₹12,500
Shared accommodations or affordable flats with flatmates.
Groceries & Food
20-25%
₹10,000 - ₹12,500
Focus on essential groceries; limited dining out.
Utilities
5-7%
₹2,500 - ₹3,500
Electricity, water, internet, and mobile bills.
Transport
8-10%
₹4,000 - ₹5,000
Public transport or fuel for two-wheelers.
Healthcare
3-5%
₹1,500 - ₹2,500
Basic health insurance or out-of-pocket expenses.
Savings
15-20%
₹7,500 - ₹10,000
Prioritize building an emergency fund and savings.
Entertainment & Miscellaneous
5-7%
₹2,500 - ₹3,500
Occasional outings, subscriptions, etc.
College Debts
5-8%
₹2,500 - ₹4,000
Student loan repayments (if applicable).
Personal Expenses
3-5%
₹1,500 - ₹2,500
Clothing, grooming, etc.

2. ₹6-12 LPA (₹50,001 - ₹1,00,000 per month)
Category
Percentage
Amount (₹)
Description
Housing (Rent)
15-20%
₹7,500 - ₹20,000
Comfortable shared apartments.
Groceries & Food
15-20%
₹7,500 - ₹20,000
Balanced spending with occasional dining out.
Utilities
5-7%
₹2,500 - ₹7,000
High-speed internet and multiple utilities.
Transport
8-10%
₹4,000 - ₹10,000
Own two-wheeler or occasional cabs.
Healthcare
3-5%
₹1,500 - ₹5,000
Health insurance with wider coverage.
Savings
20-25%
₹10,000 - ₹25,000
Build strong savings and start small investments.
Entertainment & Miscellaneous
7-10%
₹5,000 - ₹10,000
Leisure activities, subscriptions, etc.
College Debts
5-7%
₹2,500 - ₹7,000
Repay student loans (if applicable).
Personal Expenses
3-5%
₹1,500 - ₹5,000
Upgraded personal care and lifestyle.

3. ₹12-18 LPA (₹1,00,001 - ₹1,50,000 per month)
Category
Percentage
Amount (₹)
Description
Housing (Rent)
15-18%
₹15,000 - ₹27,000
Premium shared accommodations or small private apartments.
Groceries & Food
10-15%
₹10,000 - ₹22,500
Regular dining out and quality groceries.
Utilities
5-7%
₹5,000 - ₹10,500
High-speed internet, premium services.
Transport
10-12%
₹10,000 - ₹18,000
Own vehicle with regular maintenance.
Healthcare
3-5%
₹3,000 - ₹7,500
Comprehensive health insurance.
Savings & Investments
25-30%
₹25,000 - ₹45,000
Significant savings and diversified investments.
Entertainment & Miscellaneous
8-10%
₹8,000 - ₹15,000
Leisure activities, travel, and hobbies.
College Debts
5-7%
₹5,000 - ₹10,500
Loan repayments or savings toward further education.
Personal Expenses
3-5%
₹3,000 - ₹7,500
Personal care, grooming, and lifestyle.

4. ₹18-30 LPA (₹1,50,001 - ₹2,50,000 per month)
Category
Percentage
Amount (₹)
Description
Housing (Rent)
12-15%
₹18,000 - ₹37,500
High-end shared apartments or prime location flats.
Groceries & Food
10-12%
₹15,000 - ₹30,000
Premium groceries and frequent dining out.
Utilities
5-7%
₹7,500 - ₹17,500
Enhanced utilities, smart home systems, etc.
Transport
10-12%
₹15,000 - ₹30,000
Luxury car or high-end vehicle maintenance.
Healthcare
3-5%
₹7,500 - ₹12,500
Comprehensive insurance and wellness programs.
Savings & Investments
30-35%
₹45,000 - ₹87,500
Aggressive savings and high-return investments.
Entertainment & Miscellaneous
10-12%
₹15,000 - ₹30,000
Leisure travel, hobbies, and luxury entertainment.
College Debts
5-7%
₹7,500 - ₹17,500
Pay off loans faster or save for future goals.
Personal Expenses
3-5%
₹7,500 - ₹12,500
High-end personal care and grooming.

5. ₹30+ LPA (Above ₹2,50,000 per month)
Category
Percentage
Amount (₹)
Description
Housing (Rent)
10-12%
₹25,000 - ₹45,000
Luxurious apartments or top-tier properties.
Groceries & Food
8-10%
₹20,000 - ₹40,000
Gourmet dining, organic foods, personal chef options.
Utilities
5-7%
₹12,500 - ₹17,500
Top-tier utilities and services, smart home systems.
Transport
8-10%
₹25,000 - ₹45,000
Luxury car with chauffeur or premium maintenance.
Healthcare
3-5%
₹7,500 - ₹12,500
Premium healthcare and wellness services.
Savings & Investments
35-40%
₹87,500 - ₹1,00,000+
Extensive investments in various high-return avenues.
Entertainment & Miscellaneous
10-12%
₹25,000 - ₹45,000
Luxury vacations, exclusive memberships, hobbies.
College Debts
5-7%
₹12,500 - ₹17,500
Rapid loan repayments or further education savings.
Personal Expenses
3-5%
₹7,500 - ₹15,000
Luxury lifestyle and personal care.


	

1. Older Individuals (Ages 35-50+)
Up to ₹12 LPA (₹0 - ₹1,00,000 per month)
Housing (Rent): 20-25% | ₹15,000 - ₹25,000
More private or better-quality accommodation; less emphasis on flatmates.
Groceries & Food: 15-20% | ₹10,000 - ₹20,000
Focus on home-cooked meals, quality groceries, and occasional dining out.
Utilities: 7-10% | ₹7,000 - ₹10,000
Includes internet, electricity, mobile, etc., with possible higher spending for home appliances.
Healthcare: 7-10% | ₹7,000 - ₹10,000
Increasing healthcare costs, including better health insurance and preventive care.
Transport: 10-12% | ₹10,000 - ₹12,000
Car ownership becomes more common, with fuel and maintenance costs.
Savings & Investments: 20-25% | ₹20,000 - ₹25,000
Aggressive savings, investments, and retirement planning.
Entertainment & Miscellaneous: 7-10% | ₹7,000 - ₹10,000
Vacations, hobbies, and leisure activities.
College Debts (or Other Loans): 5-7% | ₹5,000 - ₹7,000
Repayment of old loans or saving for children's education.
Personal Expenses: 3-5% | ₹3,000 - ₹5,000
Grooming, clothing, and personal care.
2. Married Couples Without Children
₹12-18 LPA (₹1,00,000 - ₹1,50,000 per month)
Housing (Rent): 20-25% | ₹20,000 - ₹30,000
Larger private accommodations, occasionally in better locations.
Groceries & Food: 15-20% | ₹15,000 - ₹25,000
High-quality groceries, occasional dining out, and dining at home.
Utilities: 7-10% | ₹7,000 - ₹15,000
Enhanced utilities with higher usage (e.g., streaming services).
Healthcare: 7-10% | ₹7,000 - ₹15,000
Comprehensive insurance for both individuals, focusing on preventive care.
Transport: 10-12% | ₹10,000 - ₹18,000
Two vehicles or car maintenance costs for better-quality vehicles.
Savings & Investments: 25-30% | ₹25,000 - ₹45,000
Strong focus on long-term savings, investments, and retirement.
Entertainment & Miscellaneous: 10-12% | ₹10,000 - ₹18,000
Occasional vacations, leisure activities, hobbies, and memberships.
College Debts (or Other Loans): 5-7% | ₹5,000 - ₹10,000
Loan repayments or savings for further education or housing.
Personal Expenses: 5-7% | ₹5,000 - ₹10,000
Grooming, clothing, personal care, and home-related purchases.
3. Married Couples with Young Children
₹18-30 LPA (₹1,50,000 - ₹2,50,000 per month)
Housing (Rent): 20-25% | ₹30,000 - ₹50,000
Larger homes with space for children or high-quality flats.
Groceries & Food: 15-20% | ₹20,000 - ₹40,000
Focus on family groceries, organic food, and dining at home with occasional dining out.
Utilities: 7-10% | ₹10,000 - ₹20,000
Higher utility expenses with children, including internet, entertainment, and gadgets.
Healthcare: 10-12% | ₹15,000 - ₹25,000
Comprehensive health insurance, doctor visits, child vaccinations.
Transport: 12-15% | ₹20,000 - ₹30,000
Family car, child safety equipment, and maintenance.
Savings & Investments: 25-30% | ₹45,000 - ₹75,000
Emphasis on children's education funds, family savings, and future investments.
Entertainment & Miscellaneous: 10-12% | ₹15,000 - ₹30,000
Family vacations, children’s activities, toys, and hobbies.
College Debts (or Other Loans): 5-7% | ₹10,000 - ₹17,500
Repayment of loans or savings toward further education or a house.
Personal Expenses: 5-7% | ₹7,500 - ₹15,000
Family-related personal care, grooming, and household items.
4. Married Couples with Teen Children
₹30+ LPA (Above ₹2,50,000 per month)
Housing (Rent): 15-20% | ₹40,000 - ₹75,000
Premium houses or large apartments in prime locations.
Groceries & Food: 12-15% | ₹35,000 - ₹50,000
High-quality groceries, dining out, and more frequent food purchases for teenagers.
Utilities: 8-10% | ₹20,000 - ₹30,000
Increased utility costs with teenage children (gadgets, entertainment, etc.).
Healthcare: 10-12% | ₹25,000 - ₹40,000
Full family health coverage, orthodontics, check-ups for kids, wellness programs.
Transport: 12-15% | ₹30,000 - ₹45,000
Family cars and possible extra vehicle for teenage driving.
Savings & Investments: 30-35% | ₹1,00,000+
High savings for college funds, retirement, and large investments.
Entertainment & Miscellaneous: 10-12% | ₹30,000 - ₹45,000
Family vacations, hobby-related activities, entertainment, and gadgets for children.
College Debts (or Other Loans): 7-10% | ₹15,000 - ₹25,000
Preparing for children's college or repaying existing family loans.
Personal Expenses: 5-7% | ₹10,000 - ₹25,000
Family-related personal expenses, grooming, and extracurricular activities for children.

5. Child Expense Table Based on Age Group
0-5 Years (Infants and Toddlers)
Daycare/Nanny Costs: ₹10,000 - ₹25,000 (if both parents are working)
Healthcare: ₹5,000 - ₹15,000 (pediatric visits, vaccinations)
Education/Childcare: ₹5,000 - ₹10,000 (play schools, early education)
Miscellaneous (Clothing, Toys): ₹5,000 - ₹10,000
6-12 Years (School Age)
Education: ₹15,000 - ₹30,000 (school fees, tuition, extracurriculars)
Healthcare: ₹7,500 - ₹12,500 (routine check-ups, dental care)
Sports/Activities: ₹5,000 - ₹10,000 (sports equipment, music classes)
Miscellaneous (Clothing, Toys, Gadgets): ₹7,500 - ₹15,000
13-18 Years (Teenagers)
Education: ₹25,000 - ₹50,000 (high school, coaching classes, extracurriculars)
Healthcare: ₹7,500 - ₹15,000 (braces, routine check-ups)
Transport: ₹10,000 - ₹25,000 (driving lessons, car/bike maintenance if applicable)
Miscellaneous (Clothing, Gadgets, Entertainment): ₹10,000 - ₹25,000



### Tasks:
1. Prepare a savings plan detailing monthly and annual savings potential.
2. Compare spending with provided benchmarks and offer suggestions for reducing expenses.
3. Briefly plan saving stratgies for career_changes,major_purchases and life_events based on user data in detail and more specific way.
4. Suggest user data specific tax saving reccomendations.


### Additional Information:
- Use the data provided to suggest improvements in budgeting and investment strategies.
- Consider default values based on the user’s monthly net income bracket.
- Make sure to output in Json Format.
    """
)

# Example user data
user_data = {
    "monthly_net_income": "₹60,000",
    "other_income_sources": "Rent: ₹10,000",
    "age": "30",
    "marital_status": "Single",
    "dependents": "0",
    "housing": "₹15,000",
    "utilities": "₹3,000",
    "transport": "₹5,000",
    "insurance": "₹2,500",
    "loan_payments": "₹10,000",
    "subscriptions": "₹1,000",
    "college_debts": "₹3,000",
    "groceries": "₹8,000",
    "dining_out": "₹2,000",
    "entertainment": "₹1,500",
    "personal_care": "₹1,000",
    "travel": "₹2,500",
    "miscellaneous": "₹1,500",
    "outstanding_debt": "Credit Card: ₹20,000",
    "interest_rates": "15%",
    "loan_tenure": "6 months",
    "prioritization": "Saving for emergencies and investment in mutual funds",
    "career_changes": "Expected raise in 6 months",
    "major_purchases": "Planning to buy a car in 1 year",
    "life_events": "Getting married in 2 years",
    "percent": "20%",
    "yes_no": "Yes",
    "investment_risk": "Moderate"
}

# Initialize the chain
chain = LLMChain(llm=chat_model, prompt=investment_planning_prompt)

# Generate the response
response = chain.run(user_data)

# Output the response
print(response)
