from django.contrib import admin
from .models import PersonalInformation, IncomeDetails, Expenses, SIGoal,UserQus
# Register your models here.

admin.site.register(PersonalInformation)
admin.site.register(IncomeDetails)
admin.site.register(Expenses)
admin.site.register(SIGoal)
admin.site.register(UserQus)
admin.site.site_header = "ProfitSutra Admin"
admin.site.site_title = "ProfitSutra Admin Portal"
admin.site.index_title = "Welcome to ProfitSutra Admin Portal"

