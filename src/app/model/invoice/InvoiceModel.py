from datetime import date
from typing import Callable
from src.app.model.customer.CustomerModel import CustomerModel

from src.app.model.product.ProductModel import ProductAntibioticModel, ProductFertilizerControlModel, ProductModel, ProductNoneModel, ProductPlagueControlModel


class InvoiceLineModel:
    
    def __init__(self) -> None:
        self.id: str
        self.product: ProductModel
        self.quantity: float
        self.totalAmount: float

    def setProduct(self, product: ProductModel):
        self.product = product
        self.totalAmount = product.price * self.quantity


class InvoiceModel:

    def __init__(self) -> None:
        self.id = ""
        self.createdAt: date = date.today()
        self.totalAmount: float = 0
        self.lines: dict[str, InvoiceLineModel] = {}
        self.customer: CustomerModel 

    def setCustomer(self, customer: CustomerModel):
        self.customer = customer

    def addLine(self, invoiceLine: InvoiceLineModel):
        
        if invoiceLine.product.id in self.lines.keys():
            self.lines[invoiceLine.product.id].quantity += invoiceLine.quantity
            self.lines[invoiceLine.product.id].totalAmount += invoiceLine.totalAmount
        else:
            self.lines[invoiceLine.product.id] = invoiceLine

        self.totalAmount += invoiceLine.totalAmount

    def deleteLine(self, invoiceLine: InvoiceLineModel):
        if invoiceLine.product.id in self.lines.keys():
            del self.lines[invoiceLine.product.id]

    def forEachLine(self, linesCB: Callable[[InvoiceLineModel], None]):
        for invoiceLine in self.lines.values():
            linesCB(invoiceLine)