from typing import List

from money_assistant.transactions.models import Transaction


class TransactionEnrichService:
    @classmethod
    def _is_match(cls, name: str, keywords: List[str]) -> bool:
        normalised_transaction = name.lower().strip()
        for keyword in keywords:
            if keyword.lower().strip() in normalised_transaction:
                return True
        return False

    @classmethod
    def enrich_transactions_with_categories(cls, account_id: int, mappings: dict):
        for transaction in Transaction.objects.filter(account_id=account_id):
            for category_id, keywords in mappings.items():
                if cls._is_match(transaction.name, keywords):
                    transaction.category_id = category_id
                    transaction.save(update_fields=["category_id"])
