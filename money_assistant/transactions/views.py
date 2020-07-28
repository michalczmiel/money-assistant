from rest_framework import viewsets, status
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

import django_rq

from money_assistant.transactions.serializers import (
    AccountSerializer,
    CategorySerializer,
    TransactionSerializer,
)
from money_assistant.transactions.enriching.serializers import (
    TransactionEnrichSerializer,
)
from money_assistant.transactions.importing.services import TransactionImportService
from money_assistant.transactions.importing.serializers import (
    TransactionImportSerializer,
)
from money_assistant.transactions.analyzing.services import TransactionAnalysisService
from money_assistant.transactions.models import Account, Category, Transaction


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filterset_fields = ("account", "category", "kind")
    search_fields = ("name",)
    ordering_fields = (
        "value",
        "made_at",
    )

    @action(detail=False, url_path="import", methods=["get", "post"])
    def get_available_importers(self, request: Request) -> Response:
        if request.method == "GET":
            return Response(TransactionImportService.get_importer_types())
        elif request.method == "POST":
            file = request.FILES.get("file")
            if not file:
                raise ValidationError(detail={"file": ["This field is required."]})
            serializer = TransactionImportSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                django_rq.enqueue(
                    "money_assistant.transactions.importing.jobs.import_transactions_from_file",
                    file=file,
                    account_id=serializer.account_id,
                    importer_type=serializer.importer_type,
                )
            return Response("Success", status=status.HTTP_200_OK)

    @action(detail=False, url_path="enrich", methods=["post"])
    def map_categories(self, request: Request) -> Response:
        serializer = TransactionEnrichSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            django_rq.enqueue(
                "money_assistant.transactions.enriching.jobs.enrich_transactions_with_categories",
                account_id=serializer.data["account_id"],
                mappings=serializer.data["mappings"],
            )

        return Response("Success", status=status.HTTP_200_OK)

    @action(detail=False, url_path="analyze", methods=["get"])
    def analyze(self, _: Request) -> Response:
        return Response(TransactionAnalysisService.get_analysis())
