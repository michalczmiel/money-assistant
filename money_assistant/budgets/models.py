from django.db import models
from djmoney.models.fields import MoneyField

from money_assistant.base.models import TimeStampedModel
from money_assistant.transactions.models import Account, Category


class Budget(TimeStampedModel):
    name = models.CharField(max_length=120)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class BudgetCategory(TimeStampedModel):
    value = MoneyField(max_digits=10, decimal_places=2)
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name="categories"
    )
    priority = models.SmallIntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name
