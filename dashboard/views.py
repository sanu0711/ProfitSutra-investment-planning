from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Questionnaire.models import UserQus
# Create your views here.

@login_required(login_url='sign_in')       
def dashboard_view(request):
    user_info = UserQus.objects.get(user=request.user)
    if user_info.flag == False:
        return render(request, 'questionnaire.html')
    expanse = user_info.expenses
    
    
  
    context = {
        'raw_data': user_info
    }
    return render(request, 'dashboard.html', context)




def dashboard_view_old(request):
    user_info = UserQus.objects.get(user=request.user)
    if user_info.flag == False:
        return render(request, 'questionnaire.html')
    expanse = user_info.expenses
    expense_data ={
        'labels' : [],
        'values'  : []
    }
    for i in expanse.__dict__.items():
        if i[0] == '_state' or i[0] == 'id':
            continue
        if i[1] == 0:
            continue
        expense_data['labels'].append(i[0])
        expense_data['values'].append(i[1])
           
    user_data = UserQus.objects.filter(
        user=request.user).select_related(
           'user',
            'personal_information',
            'income_details',
            'expenses',
            'savings_investment_goals'
    ).values(
        'user__username',
        'user__email',
        'personal_information__first_name',
        'personal_information__last_name',
        'personal_information__dob',
        'personal_information__marital_status',
        'personal_information__dependents',
        'personal_information__employment_status',
        'income_details__monthly_income',
        'income_details__other_income',
        'income_details__other_income_type',
        'income_details__other_income_amount',
        'income_details__other_income_frequency',
        'expenses__rent',
        'expenses__utilities',
        'expenses__insurance',
        'expenses__transportation',
        'expenses__food',
        'expenses__healthcare',
        'expenses__education',
        'expenses__entertainment',
        'expenses__savings',
        'expenses__loan',
        'savings_investment_goals__savings_goal',
        'savings_investment_goals__investment_goal',
        'savings_investment_goals__investment_horizon',
        'savings_investment_goals__risk_tolerance',
        'savings_investment_goals__investment_knowledge',
        'savings_investment_goals__investment_experience',
        'savings_investment_goals__investment_objective',
        'savings_investment_goals__investment_strategy',
        'savings_investment_goals__investment_style',
        'savings_investment_goals__investment_amount',
        'savings_investment_goals__investment_frequency',
        'savings_investment_goals__investment_start_date',
        'savings_investment_goals__investment_end_date',
        'savings_investment_goals__investment_account',
        'savings_investment_goals__investment_account_type',
        'savings_investment_goals__investment_account_balance'
        
    )
    
    # print(user_data)
    
  
    context = {
        'user_info': user_data[0],
        'expense_data': expense_data,
        # 'total_expense': total_expense,
        'raw_data': user_info
    }
    return render(request, 'dashboard.html', context)