from rest_framework import serializers


class TransactionImportSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    importer_type = serializers.CharField(max_length=10)
