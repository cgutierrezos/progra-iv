
from src.app.model.invoice.InvoiceModel import InvoiceLineModel, InvoiceModel
from src.app.model.invoice.InvoiceModelCollection import InvoiceModelCollection
from faker import Faker
from uuid import uuid4


class InvoiceLineModelFactory:

    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def build(self) -> InvoiceLineModel:

        invoiceLine = InvoiceLineModel()
        invoiceLine.id = str(uuid4())
        invoiceLine.quantity = float(str(self.faker.random_int(2, 5)))

        return invoiceLine
        
        

class InvoiceModelFactory:

    def __init__(self, faker: Faker) -> None:
        self.faker = faker
        self.invoiceLineFactory = InvoiceLineModelFactory(self.faker)

    def build(self) -> InvoiceModel:
        
        invoice = InvoiceModel()

        invoice.id = str(uuid4())
        invoice.createdAt = self.faker.date()
        invoice.totalAmount = 0

        return invoice

    def buildMany(self, num: int) -> InvoiceModelCollection:
        
        invoices = InvoiceModelCollection()

        for i in range(num):
            invoices.add(self.build())

        return invoices