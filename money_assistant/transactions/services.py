from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


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


def import_transactions_from_file(file, account_id: int, importer_type: str):
    importer_class = CSV_IMPORTERS.get(importer_type)
    importer = importer_class()
    importer.process(file=file, account_id=account_id)


def is_match(name: str, keywords: List[str]) -> bool:
    normalised_transaction = name.lower().strip()
    for keyword in keywords:
        if keyword.lower().strip() in normalised_transaction:
            return True
    return False


def enrich_transactions_with_categories(account_id: int, mappings: dict):
    for transaction in Transaction.objects.filter(account_id=account_id):
        for category_id, keywords in mappings.items():
            if is_match(transaction.name, keywords):
                transaction.category_id = category_id
                transaction.save(update_fields=["category_id"])
