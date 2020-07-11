import statistics
from collections import defaultdict
from typing import Optional
from decimal import Decimal

from money_assistant.transactions.models import Transaction


class TransactionAnalysisService:
    @classmethod
    def _get_spending_statistics(cls) -> Optional[dict]:
        transactions = Transaction.expenses.all()

        if not transactions:
            return None

        spending_by_category = defaultdict(Decimal)
        spending_values = []

        for transaction in transactions:
            category_key = transaction.category_id or -1
            amount = abs(transaction.value.amount)
            spending_values.append(amount)
            spending_by_category[category_key] += amount

        spending_statistics = {
            "count": len(spending_values),
            "sum": sum(spending_values),
            "min": min(spending_values),
            "max": max(spending_values),
            "mean": round(statistics.mean(spending_values), 2),
            "median": statistics.median(spending_values),
            "std": round(statistics.stdev(spending_values), 2),
        }

        return {"analyzing": spending_statistics, "by_category": spending_by_category}

    @classmethod
    def get_analysis(cls):
        return {
            "spending": cls._get_spending_statistics(),
        }
