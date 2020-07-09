from rest_framework import viewsets

from money_assistant.budgets.serializers import (
    BudgetSerializer,
    BudgetCategorySerializer,
)
from money_assistant.budgets.models import Budget, BudgetCategory


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
