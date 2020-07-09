from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request

from money_assistant.statistics.services import StatisticsService


class StatisticsView(ViewSet):
    def list(self, request: Request):
        return Response({"spending": StatisticsService.get_spending_statistics()})
