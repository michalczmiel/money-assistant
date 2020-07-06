from rest_framework import serializers

from money_assistant.transactions.models import Account, Category, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "name", "created_at", "modified_at")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "created_at", "modified_at")


class TransactionImportSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    importer_type = serializers.CharField(max_length=10)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "name",
            "value",
            "account",
            "category",
            "kind",
            "made_at",
            "created_at",
            "modified_at",
        )
