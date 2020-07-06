from typing import Union

from django.db import models
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

    def __str__(self):
        return self.name


TransactionKind = Union[Transaction.CARD, Transaction.TRANSFER, Transaction.CASH]
