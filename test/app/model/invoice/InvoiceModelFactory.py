from src.app.model.customer.CustomerModel import CustomerModel
from src.app.model.invoice.InvoiceModel import InvoiceLineModel, InvoiceModel
from src.app.model.invoice.InvoiceModelCollection import InvoiceModelCollection
from faker import Faker
from uuid import uuid4

from src.app.model.product.ProductModel import ProductAntibioticModel, ProductFertilizerControlModel, ProductPlagueControlModel
from test.app.model.customer.CustomerModelFactory import CustomerModelFactory
from test.app.model.product.ProductModelFactory import ProductModelFactory


class InvoiceLineModelFactory:

    def __init__(self, faker: Faker) -> None:
        self.faker = faker
        self.productFactory = ProductModelFactory(self.faker)

    def build(self) -> InvoiceLineModel:

        invoiceLine = InvoiceLineModel()
        invoiceLine.id = str(uuid4())
        invoiceLine.quantity = float(str(self.faker.random_int(2, 5)))
        invoiceLine.setProduct(self.productFactory.build())

        return invoiceLine
        
        

class InvoiceModelFactory:

    def __init__(self, faker: Faker) -> None:
        self.faker = faker
        self.customerFactory = CustomerModelFactory(self.faker)
        self.invoiceLineFactory = InvoiceLineModelFactory(self.faker)

    def build(self) -> InvoiceModel:
        
        invoice = InvoiceModel()

        invoice.id = str(uuid4())
        invoice.createdAt = self.faker.date()
        invoice.totalAmount = 0
        invoice.setCustomer(self.customerFactory.build())
        linesCount = self.faker.random_int(2, 5)
        for i in range(linesCount):
            invoice.addLine(self.invoiceLineFactory.build())

        return invoice

    def buildMany(self, num: int) -> InvoiceModelCollection:
        
        invoices = InvoiceModelCollection()

        for i in range(num):
            invoices.add(self.build())

        return invoices