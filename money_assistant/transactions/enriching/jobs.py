from django_rq import job

from money_assistant.transactions.enriching.services import TransactionEnrichService


@job
def enrich_transactions_with_categories(account_id, mappings):
    TransactionEnrichService.enrich_transactions_with_categories(
        account_id=account_id, mappings=mappings,
    )
