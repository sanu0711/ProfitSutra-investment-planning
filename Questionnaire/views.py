from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
# from .chatbot import response_q
from .tests import chat_to_query
from .models import PersonalInformation, IncomeDetails, Expenses, SIGoal, UserQus
# Create your views here.
def home(request): 
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            user_qus = UserQus.objects.get(user=user)
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'home.html')
        if not user_qus.flag:
            messages.info(request, "Please complete the questionnaire to proceed")
    return render(request, 'home.html')

def chatbot_view(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            response = chat_to_query(question)
            return render(request, 'chatbot.html', {
                'response': response,
                'qus': question})
        else:
            messages.error(request, "Please enter a question to get response")
            return render(request, 'chatbot.html')    
    return render(request, 'chatbot.html')
  
  
def questionnaire_view(request):
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
            
            # Savings and Investment Goals
            savings_goal = request.POST.get('savings_goal')
            investment_goal = request.POST.get('investment_goal')
            investment_horizon = request.POST.get('investment_horizon')
            risk_tolerance = request.POST.get('risk_tolerance')
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
              
            personal_info = PersonalInformation(first_name=first_name, last_name=last_name, dob=dob, marital_status=marital_status, dependents=dependents, employment_status=employment_status)
            income_info = IncomeDetails(monthly_income=monthly_income, other_income=other_income, other_income_type=other_income_type, other_income_amount=other_income_amount, other_income_frequency=other_income_frequency)
            expenses_info = Expenses(rent=rent, utilities=utilities, insurance=insurance, transportation=transportation, food=food, healthcare=healthcare, education=education, entertainment=entertainment, savings=savings, loan=loan)
            savings_investment_goal = SIGoal(savings_goal=savings_goal, investment_goal=investment_goal, investment_horizon=investment_horizon, risk_tolerance=risk_tolerance, investment_knowledge=investment_knowledge, investment_experience=investment_experience, investment_objective=investment_objective, investment_strategy=investment_strategy, investment_style=investment_style, investment_amount=investment_amount, investment_frequency=investment_frequency, investment_start_date=investment_start_date, investment_end_date=investment_end_date, investment_account=investment_account, investment_account_type=investment_account_type, investment_account_balance=investment_account_balance)
            
            personal_info.save()
            income_info.save()
            expenses_info.save()
            savings_investment_goal.save()
            
            messages.success(request, "Data saved successfully")
            
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
            user_qus.save()
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'questionnaire.html')
    return render(request, 'questionnaire.html')

