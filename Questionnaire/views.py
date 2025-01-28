from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .tests import chat_to_query
from .suggestion_questinare import suggestion_to_questnior
from django.contrib.auth.decorators import login_required
from .models import PersonalInformation, IncomeDetails, Expenses, SIGoal, UserQus, QuesHistory
from .agent_ai_tools import run_agent
# from .qus_to_query import chat_to_query

# from dashboard.tests import read_data

# Create your views here.
def home(request):
    # message = read_data()
    # print(message) 
    return render(request, 'home.html')

@login_required(login_url='sign_in') 
def chatbot_view(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            response = chat_to_query(question)
            # response = 'Give me complete analysis(from all tools) of nmdc'
            # agent2 = run_agent(response)
            # print(agent2)
            return render(request, 'chatbot.html', {
                'response': response,
                # 'response': agent2,
                
                'qus': question})
        else:
            messages.error(request, "Please enter a question to get response")
            return render(request, 'chatbot.html')    
    return render(request, 'chatbot.html')

@login_required(login_url='sign_in')
def research_view(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            # response = 'Give me complete analysis(from all tools) of nmdc'
            agent2 = run_agent(question)
            # print(agent2)
            output = agent2
            output = output.replace("```html", "")
            output = output.replace("```", "")
            output = output.replace("\n", "")
            return render(request, 'stock_research.html', {
                'response': output,
                'qus': question})
        else:
            messages.error(request, "Please enter a question to get response")
            return render(request, 'stock_research.html')    
    return render(request, 'stock_research.html')
  
@login_required(login_url='sign_in')
def questionnaire_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        marital_status = request.POST.get('marital_status')
        dependents = request.POST.get('dependents')
        employment_status = request.POST.get('employment_status')
        
        monthly_income = request.POST.get('monthly_income')
        other_income = request.POST.get('other_income')
        other_income_type = request.POST.get('other_income_type')
        other_income_frequency = request.POST.get('other_income_frequency')
        
        rent = request.POST.get('rent')
        utilities = request.POST.get('utilities')
        insurance = request.POST.get('insurance')
        transportation = request.POST.get('transportation')
        food = request.POST.get('food')
        healthcare = request.POST.get('healthcare')
        education = request.POST.get('education')
        entertainment = request.POST.get('entertainment')

        loan = request.POST.get('loan')
        loan_tenure = request.POST.get('loan_tenure')
        loan_interest = request.POST.get('loan_interest')
        
        risk_tolerance = request.POST.get('risk_tolerance')
        prioritization = request.POST.get('prioritization')
        career_changes = request.POST.get('career_changes')
        major_purchases = request.POST.get('major_purchases')
        life_events = request.POST.get('life_events')
        
        user_data = {
            "monthly_net_income": monthly_income,
            "other_income_sources": other_income,
            "dob": dob,
            "marital_status": marital_status,
            "dependents": dependents,
            "housing": rent,
            "utilities": utilities,
            "transport": transportation,
            "insurance": insurance,
            "loan_payments": loan,
            "subscriptions": entertainment,
            "college_debts": education,
            "groceries": food,
            "dining_out": food,
            "entertainment": entertainment,
            "personal_care": healthcare,
            "travel": transportation,
            "miscellaneous": None,
            "outstanding_debt": loan,
            "interest_rates": loan_interest,
            "loan_tenure": loan_tenure,
            "prioritization": prioritization,
            "career_changes": career_changes,
            "major_purchases": major_purchases,
            "life_events": life_events,
            "percent": None,
            "yes_no": "Yes",
            "investment_risk": risk_tolerance
        }
        try:
            gen_ai = suggestion_to_questnior(user_data)
            QuesHistory.objects.create(user=request.user, user_input=user_data, ai_output=gen_ai)
            return render(request, 'questionnaire_out.html', {'gen_ai': gen_ai})
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'questionnaire.html')
    return render(request, 'questionnaire.html')

@login_required(login_url='sign_in')
def ques_history_view(request):
    if QuesHistory.objects.filter(user=request.user).exists():
        history = QuesHistory.objects.filter(user=request.user)
        return render(request, 'ques_history.html', {'history': history})
    else:
        messages.info(request, "No history found")
        return render(request, 'ques_history.html')

@login_required(login_url='sign_in')
def ques_explore(request, id):
    if QuesHistory.objects.filter(id=id).exists():
        history = QuesHistory.objects.get(id=id)
        return render(request, 'ques_explore.html', {'history': history})
    else:
        messages.info(request, "No history found")
        return render(request, 'ques_history.html')

def questionnaire_view_old(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to complete the questionnaire")
        return redirect('sign_in')
    else:
        if UserQus.objects.filter(user=request.user).exists():
            user = User.objects.get(username=request.user)
            user_qus = UserQus.objects.get(user=user)
            if user_qus.flag:
                return redirect('dashboard')
            
    if request.method == 'POST':
        try:
            user_input = request.POST
            user = User.objects.get(username=request.user)
            # personal details
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            dob = request.POST.get('dob')
            marital_status = request.POST.get('marital_status')
            dependents = request.POST.get('dependents')
            employment_status = request.POST.get('employment_status')
            # Income Details
            monthly_income = request.POST.get('monthly_income')
            other_income = request.POST.get('other_income')
            other_income_type = request.POST.get('other_income_type')
            other_income_amount = request.POST.get('other_income_amount')
            other_income_frequency = request.POST.get('other_income_frequency')
            
            # Expenses
            rent = request.POST.get('rent')
            utilities = request.POST.get('utilities')
            insurance = request.POST.get('insurance')
            transportation = request.POST.get('transportation')
            food = request.POST.get('food')
            healthcare = request.POST.get('healthcare')
            education = request.POST.get('education')
            entertainment = request.POST.get('entertainment')
            savings = request.POST.get('savings')
            loan = request.POST.get('loan')
            loan_tenure = request.POST.get('loan_tenure')
            loan_interest = request.POST.get('loan_interest')
            # Savings and Investment Goals
            risk_tolerance = request.POST.get('risk_tolerance')
            prioritization = request.POST.get('prioritization')
            career_changes = request.POST.get('career_changes')
            major_purchases = request.POST.get('major_purchases')
            life_events = request.POST.get('life_events')
            savings_goal = request.POST.get('savings_goal')
            investment_goal = request.POST.get('investment_goal')
            investment_horizon = request.POST.get('investment_horizon')
            investment_knowledge = request.POST.get('investment_knowledge')
            investment_experience = request.POST.get('investment_experience')
            investment_objective = request.POST.get('investment_objective')
            investment_strategy = request.POST.get('investment_strategy')
            investment_style = request.POST.get('investment_style')
            investment_amount = request.POST.get('investment_amount')
            investment_frequency = request.POST.get('investment_frequency')
            investment_start_date = request.POST.get('investment_start_date')
            investment_end_date = request.POST.get('investment_end_date')
            investment_account = request.POST.get('investment_account')
            investment_account_type = request.POST.get('investment_account_type')
            investment_account_balance = request.POST.get('investment_account_balance')
              
            personal_info = PersonalInformation(
                first_name=first_name, last_name=last_name, dob=dob, 
                marital_status=marital_status, dependents=dependents, 
                employment_status=employment_status,monthly_income=monthly_income, 
                other_income=other_income)
            income_info = IncomeDetails(
                monthly_income=monthly_income, other_income=other_income, 
                other_income_type=other_income_type, other_income_amount=other_income_amount, 
                other_income_frequency=other_income_frequency)
            expenses_info = Expenses(
                rent=rent, utilities=utilities, insurance=insurance, 
                transportation=transportation, food=food, healthcare=healthcare, 
                education=education, entertainment=entertainment, savings=savings, 
                loan=loan, loan_tenure=loan_tenure, loan_interest_rate=loan_interest)
            savings_investment_goal = SIGoal(
                savings_goal=savings_goal, investment_goal=investment_goal, 
                investment_horizon=investment_horizon, risk_tolerance=risk_tolerance, 
                investment_knowledge=investment_knowledge, investment_experience=investment_experience, 
                investment_objective=investment_objective, investment_strategy=investment_strategy, 
                investment_style=investment_style, investment_amount=investment_amount, investment_frequency=investment_frequency, 
                investment_start_date=investment_start_date, investment_end_date=investment_end_date, 
                investment_account=investment_account, investment_account_type=investment_account_type, 
                investment_account_balance=investment_account_balance, 
                prioritization=prioritization, career_changes=career_changes, 
                major_purchases=major_purchases, life_events=life_events)
            
            personal_info.save()
            income_info.save()
            expenses_info.save()
            savings_investment_goal.save()
            
            
            
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'questionnaire.html')
        try:
            user_qus = UserQus.objects.get(user=user)
            user_qus.personal_information = personal_info
            user_qus.income_details = income_info
            user_qus.expenses = expenses_info
            user_qus.savings_investment_goals = savings_investment_goal
            user_qus.flag = True
            # mapped_data = {
            #     'housing': rent,  
            #     'major_purchases': max(utilities, healthcare, entertainment),
            #     'dob': dob, 
            #     'marital_status': marital_status,
            #     'entertainment': entertainment,
            #     'utilities': utilities,
            #     'dependents': dependents,
            #     'insurance': insurance,
            #     'college_debts': education,
            #     'transport': transportation,
            #     'dining_out': food,
            #     'prioritization': investment_objective,
            #     'monthly_net_income': monthly_income,
            #     'life_events': marital_status,
            #     'investment_risk': risk_tolerance,
            #     'outstanding_debt': loan,
            #     'travel': transportation,
            #     'loan_tenure': None, 
            #     'personal_care': healthcare,
            #     'loan_payments': loan,
            #     'interest_rates': None, 
            #     'other_income_sources': other_income,
            #     'groceries': food,
            #     'subscriptions': entertainment,
            #     'percent': None, 
            #     'yes_no': None, 
            #     'miscellaneous': None,
            #     'career_changes': employment_status,
            # }
            # gen_ai = suggestion_to_questnior(mapped_data)
            # user_qus.advice = gen_ai
            user_qus.save()
            messages.success(request, "Data saved successfully")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'questionnaire.html')
    return render(request, 'questionnaire.html')

