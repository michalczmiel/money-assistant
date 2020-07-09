from typing import Union

from django.db import models
from djmoney.money import Money
from djmoney.models.fields import MoneyField

from money_assistant.base.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Account(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TransactionExpensesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(value__lt=Money(0.0))


class TransactionIncomeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(value__gt=Money(0.0))


class Transaction(TimeStampedModel):
    CARD = "card"
    CASH = "cash"
    TRANSFER = "transfer"
    KIND = ((CARD, "Card"), (CASH, "Cash"), (TRANSFER, "Transfer"))

    name = models.CharField(max_length=120)
    value = MoneyField(max_digits=10, decimal_places=2)
    made_at = models.DateField(blank=True, null=True)
    kind = models.CharField(max_length=10, choices=KIND, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )

    objects = models.Manager()
    income = TransactionIncomeManager()
    expenses = TransactionExpensesManager()

    def __str__(self):
        return self.name


TransactionKind = Union[Transaction.CARD, Transaction.TRANSFER, Transaction.CASH]
