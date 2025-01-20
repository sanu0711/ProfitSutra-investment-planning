from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PersonalInformation(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=100, null=True, blank=True)
    dependents = models.IntegerField(null=True, blank=True, default=0)
    employment_status = models.CharField(max_length=100, null=True, blank=True)
    monthly_income = models.FloatField(null=True, blank=True)
    other_income = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.first_name
    class Meta:
        managed = True
        db_table = 'personal_information'
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"

       
class IncomeDetails(models.Model):
    monthly_income = models.FloatField(null=True, blank=True)
    other_income = models.CharField(max_length=100, null=True, blank=True)
    other_income_type = models.CharField(max_length=100, null=True, blank=True)
    other_income_amount = models.FloatField(null=True, blank=True)
    other_income_frequency = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'
    class Meta:
        managed = True
        db_table = 'income_details'
        verbose_name = "Income Details"
        verbose_name_plural = "Income Details"
        

  

class Expenses(models.Model):
    rent = models.FloatField(null=True, blank=True)
    utilities = models.FloatField(null=True, blank=True)
    insurance = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    food = models.FloatField(null=True, blank=True)
    healthcare = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    entertainment = models.FloatField(null=True, blank=True)
    savings = models.FloatField(null=True, blank=True)
    loan = models.FloatField(null=True, blank=True)
    loan_tenure = models.CharField(max_length=100, null=True, blank=True)
    loan_interest_rate = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'
    class Meta:
        managed = True
        db_table = 'expenses'
        verbose_name = "Expenses"
        verbose_name_plural = "Expenses"
        

class SIGoal(models.Model):
    risk_tolerance = models.CharField(max_length=100, null=True, blank=True)
    prioritization = models.CharField(max_length=100, null=True, blank=True)
    career_changes = models.CharField(max_length=100, null=True, blank=True)
    major_purchases = models.CharField(max_length=100, null=True, blank=True)
    life_events = models.CharField(max_length=100, null=True, blank=True)
    savings_goal = models.FloatField(null=True, blank=True)
    investment_goal = models.FloatField(null=True, blank=True)
    investment_horizon = models.CharField(max_length=100, null=True, blank=True)
    investment_knowledge = models.CharField(max_length=100, null=True, blank=True)
    investment_experience = models.CharField(max_length=100, null=True, blank=True)
    investment_objective = models.CharField(max_length=100, null=True, blank=True)
    investment_strategy = models.CharField(max_length=100, null=True, blank=True)
    investment_style = models.CharField(max_length=100, null=True, blank=True)
    investment_amount = models.FloatField(null=True, blank=True)
    investment_frequency = models.CharField(max_length=100, null=True, blank=True)
    investment_start_date = models.DateField(null=True, blank=True)
    investment_end_date = models.DateField(null=True, blank=True)
    investment_account = models.CharField(max_length=100, null=True, blank=True)
    investment_account_type = models.CharField(max_length=100, null=True, blank=True)
    investment_account_balance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.id}'
    class Meta:
        managed = True
        db_table = 'savings_investment_goals'
        verbose_name = "Savings and Investment Goals"
        verbose_name_plural = "Savings and Investment Goals"
        

class UserQus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=100, default='User', null=True, blank=True)
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, null=True, blank=True)
    income_details = models.ForeignKey(IncomeDetails, on_delete=models.CASCADE, null=True, blank=True)
    expenses = models.ForeignKey(Expenses, on_delete=models.CASCADE, null=True, blank=True)
    savings_investment_goals = models.ForeignKey(SIGoal, on_delete=models.CASCADE, null=True, blank=True)
    advice = models.TextField(null=True, blank=True)
    flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user_name
    class Meta:
        managed = True
        db_table = 'user_questionnaire'
        verbose_name = "User Questionnaire"
        verbose_name_plural = "User Questionnaire"

class QuesHistory(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_input = models.JSONField(null=True, blank=True)
    ai_output = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    class Meta:
        managed = True
        db_table = 'questionnaire_history'
        verbose_name = "Questionnaire History"
        verbose_name_plural = "Questionnaire History"
        
