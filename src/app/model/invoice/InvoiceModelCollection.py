from typing import Callable
from src.app.model.invoice.InvoiceModel import InvoiceModel


class InvoiceModelCollection:
    
    def __init__(self) -> None:
        self.invoices: list[InvoiceModel] = []

    def add(self, invoice: InvoiceModel):
        self.invoices.append(invoice)

    def forEach(self, invoiceCB: Callable[[InvoiceModel], None]):
        for invoice in self.invoices:
            invoiceCB(invoice)

    def count(self) -> int:
        return len(self.invoices)