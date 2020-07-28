from django_rq import job

from money_assistant.transactions.importing.services import TransactionImportService


@job
def import_transactions_from_file(file, account_id, importer_type):
    TransactionImportService.import_transactions_from_file(
        file=file, account_id=account_id, importer_type=importer_type
    )
