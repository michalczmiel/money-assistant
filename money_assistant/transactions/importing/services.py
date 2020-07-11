from money_assistant.transactions.importing.importers import CSV_IMPORTERS


class TransactionImportService:
    @classmethod
    def import_transactions_from_file(cls, file, account_id: int, importer_type: str):
        importer_class = CSV_IMPORTERS.get(importer_type)
        importer = importer_class()
        importer.process(file=file, account_id=account_id)

    @classmethod
    def get_importer_types(cls) -> dict:
        importer_types = CSV_IMPORTERS.keys()

        return {
            "results": importer_types,
            "count": len(importer_types),
        }
