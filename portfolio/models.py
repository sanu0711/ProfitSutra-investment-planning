from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserStock(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    buy_date = models.DateField()

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'user_stocks'
        verbose_name = 'User Stock'
        verbose_name_plural = 'User Stocks'
        
    @property
    def total(self):
        return self.quantity * self.price
    
class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(UserStock)

    def __str__(self):
        return self.user.username
    class Meta:
        managed = True
        db_table = 'portfolios'
        verbose_name_plural = 'Portfolios'
        verbose_name = 'Portfolio'
            
    # @property
    # def total_investment(self):
    #     return sum([stock.total for stock in self.stocks.all()])