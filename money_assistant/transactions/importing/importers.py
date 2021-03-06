from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from money_assistant.transactions.models import Transaction, TransactionKind


class CSVImporter(ABC):
    @property
    @abstractmethod
    def delimiter(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def name(cls, items: List[str]) -> str:
        pass

    @classmethod
    @abstractmethod
    def kind(cls, items: List[str]) -> TransactionKind:
        pass

    @classmethod
    @abstractmethod
    def value(cls, items: List[str]) -> float:
        pass

    @classmethod
    @abstractmethod
    def made_at(cls, items: List[str]) -> datetime:
        pass

    def process(self, file, account_id: int):
        transactions = []

        for line in file:
            line = line.decode("utf-8", errors="ignore")
            if "DATA" not in line:
                continue
            items = line.split(self.delimiter)
            transaction = Transaction(
                name=self.name(items),
                made_at=self.made_at(items),
                value=self.value(items),
                kind=self.kind(items),
                account_id=account_id,
            )
            transactions.append(transaction)

        Transaction.objects.bulk_create(transactions)


class MBankCSVImporter(CSVImporter):
    delimiter = ";"

    def name(self, items: List[str]) -> str:
        value = items[3]
        return value.split("/")[0].strip().replace('"', "")

    def kind(self, items: List[str], card_keyword: str = "KARTY") -> TransactionKind:
        value = items[2]
        return Transaction.CARD if card_keyword in value else Transaction.TRANSFER

    def value(self, items: List[str]) -> float:
        value = items[6]
        if isinstance(value, float):
            return value
        return float(value.replace(",", ".").replace(" ", ""))

    def made_at(self, items: List[str]) -> datetime:
        value = items[0]
        date = datetime.strptime(value, "%Y-%m-%d")
        return date


CSV_IMPORTERS = {
    "mbank": MBankCSVImporter,
}
