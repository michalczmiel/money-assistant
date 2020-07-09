from rest_framework import routers

from money_assistant.transactions.views import (
    AccountViewSet,
    CategoryViewSet,
    TransactionViewSet,
)
from money_assistant.statistics.views import StatisticsView

router = routers.DefaultRouter()
router.register(r"accounts", AccountViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"statistics", StatisticsView, basename="statistics")
