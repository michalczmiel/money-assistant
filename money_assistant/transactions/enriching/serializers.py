from rest_framework import serializers


class TransactionEnrichSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    mappings = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField()), allow_empty=False
    )
