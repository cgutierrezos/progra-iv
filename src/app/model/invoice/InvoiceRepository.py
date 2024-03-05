from abc import ABC, abstractmethod
from datetime import datetime
from src.app.model.customer.CustomerModel import CustomerModel

from src.app.model.invoice.InvoiceModel import InvoiceLineModel, InvoiceModel
from src.app.model.invoice.InvoiceModelCollection import InvoiceModelCollection
from src.app.model.product.ProductModel import ANIMAL_TYPE_DICT, PRODUCT_TYPE, ProductAntibioticModel, ProductFertilizerControlModel, ProductPlagueControlModel
from src.providers.MySQLProvider import MySQLProvider


class InvoiceRepository(ABC):

    @abstractmethod
    def create(self, invoice: InvoiceModel):
        pass

    @abstractmethod
    def update(self, invoice: InvoiceModel):
        pass

    @abstractmethod
    def delete(self, invoice: InvoiceModel):
        pass

    @abstractmethod
    def findOneByID(self, id: str) -> InvoiceModel:
        pass

    @abstractmethod
    def findManyByCustomerIdentification(self, customerIdentification: str) -> InvoiceModelCollection:
        pass

    @abstractmethod
    def findAll(self) -> InvoiceModelCollection:
        pass

class InMemoryInvoiceRepository(InvoiceRepository):

    def __init__(self) -> None:
        super().__init__()

        self.invoices: dict[str, InvoiceModel] = {}

    def create(self, invoice: InvoiceModel):
        self.invoices[invoice.id] = invoice

    def update(self, invoice: InvoiceModel):
        if invoice.id in self.invoices.keys():
            self.invoices[invoice.id] = invoice


    def delete(self, invoice: InvoiceModel):
        if invoice.id in self.invoices.keys():
            del self.invoices[invoice.id]

    def findOneByID(self, id: str) -> InvoiceModel | None:
        if id in self.invoices.keys():
            return self.invoices[id]
        
        return None

    def findManyByCustomerIdentification(self, customerIdentification: str) -> InvoiceModelCollection:
        
        invoices = InvoiceModelCollection()
        
        for invoice in self.invoices.values():
            if customerIdentification in invoice.customer.identification:
                invoices.add(invoice)
        
        return invoices

    def findAll(self) -> InvoiceModelCollection:
        invoices = InvoiceModelCollection()
        
        for invoice in self.invoices.values():
            invoices.add(invoice)
        
        return invoices
    

class MySQLInvoiceRepository(InvoiceRepository):

    def __init__(self, mysqlProvider: MySQLProvider) -> None:
        super().__init__()
        self.mysqlProvider: MySQLProvider = mysqlProvider
        

    def create(self, invoice: InvoiceModel):
        sql: list[str] = []
        sql.append(f"INSERT INTO invoice (id, customer_id, created_at, total_amount) VALUES ('{invoice.id}', '{invoice.customer.id}', '{invoice.createdAt.strftime("%Y-%m-%d")}', {invoice.totalAmount})")
        
        invoice.forEachLine(lambda invoiceLine: sql.append(
            f"""INSERT INTO invoice_line (id, invoice_id, product_id, quantity, total_amount) VALUES ('{invoiceLine.id}', '{invoice.id}', '{invoiceLine.product.id}', {invoiceLine.quantity}, {invoiceLine.totalAmount})"""
        ))

        self.mysqlProvider.executeMany(sql)

    def update(self, invoice: InvoiceModel):
        
        sql: list[str] = []
        sql.append(f"UPDATE invoice SET customer_id='{invoice.customer.id}', created_at='{invoice.createdAt.strftime("%Y-%m-%d")}', total_amount={invoice.totalAmount} WHERE id='{invoice.id}' LIMIT 1")
        
        sql.append(f"DELETE FROM invoice WHERE id='{invoice.id}'")
        
        invoice.forEachLine(lambda invoiceLine: sql.append(
            f"INSERT INTO invoice_line (id, invoice_id, product_id, quantity, total_amount) VALUES ('{invoiceLine.id}', '{invoice.id}', {invoiceLine.quantity}, {invoiceLine.totalAmount})"
        ))

        self.mysqlProvider.execute(";\n".join(sql)+";")


    def delete(self, invoice: InvoiceModel):
        sql = f"DELETE FROM invoice WHERE id='{invoice.id}' LIMIT 1"
        self.mysqlProvider.execute(sql)


    def findOneByID(self, id: str) -> InvoiceModel | None:
        sql = f"""SELECT invoice.id AS invoice_id, invoice.created_at AS invoice_created_at, invoice.total_amount AS invoice_total_amount,
        customers.id AS customer_id, customers.identification AS customer_identification, customers.name AS customer_name,
        invoice_line.id AS line_id, invoice_line.quantity AS line_quantity, invoice_line.total_amount AS line_total_amount, 
        products.id AS product_id, products.ica AS product_ica, products.name AS product_name, products.price AS product_price, 
        products.frecuency AS product_frecuency, products.type AS product_type,
        plague_control_products.grace_period AS product_grace_period, 
        fertilizer_control_products.last_application_date AS product_last_application_date, 
        antibiotic_products.dose AS product_dose, antibiotic_products.animal_type AS product_animal_type
        FROM invoice
        INNER JOIN customers ON customers.id = invoice.customer_id
        INNER JOIN invoice_line ON invoice.id = invoice_line.invoice_id
        INNER JOIN products ON products.id = invoice_line.product_id
        LEFT JOIN plague_control_products ON plague_control_products.id = products.id
        LEFT JOIN fertilizer_control_products ON fertilizer_control_products.id = products.id
        LEFT JOIN antibiotic_products ON antibiotic_products.id = products.id
        WHERE invoice.id='{id}'"""
        rows = self.mysqlProvider.fetch(sql)

        if len(rows) == 0:
            return None
        
        return self.__deserializeInvoice(rows)

    def findManyByCustomerIdentification(self, customerIdentification: str) -> InvoiceModelCollection:
        
        sql = f"""SELECT invoice.id AS invoice_id, invoice.created_at AS invoice_created_at, invoice.total_amount AS invoice_total_amount,
        customers.id AS customer_id, customers.identification AS customer_identification, customers.name AS customer_name,
        invoice_line.id AS line_id, invoice_line.quantity AS line_quantity, invoice_line.total_amount AS line_total_amount, 
        products.id AS product_id, products.ica AS product_ica, products.name AS product_name, products.price AS product_price, 
        products.frecuency AS product_frecuency, products.type AS product_type,
        plague_control_products.grace_period AS product_grace_period, 
        fertilizer_control_products.last_application_date AS product_last_application_date, 
        antibiotic_products.dose AS product_dose, antibiotic_products.animal_type AS product_animal_type
        FROM invoice
        INNER JOIN customers ON customers.id = invoice.customer_id
        INNER JOIN invoice_line ON invoice.id = invoice_line.invoice_id
        INNER JOIN products ON products.id = invoice_line.product_id
        LEFT JOIN plague_control_products ON plague_control_products.id = products.id
        LEFT JOIN fertilizer_control_products ON fertilizer_control_products.id = products.id
        LEFT JOIN antibiotic_products ON antibiotic_products.id = products.id
        WHERE customers.identification = '{customerIdentification}'"""
        rows = self.mysqlProvider.fetch(sql)

        
        invoiceDict: dict[str, InvoiceModel] = {}

        for row in rows:
            
            invoiceID = str(row[0])
            invoice: InvoiceModel

            if invoiceID in invoiceDict.keys():
                invoice = invoiceDict[invoiceID]
            else:
                invoice = InvoiceModel()
                invoice.id = invoiceID
                invoice.createdAt = datetime.strptime(str(row[1]), "%Y-%m-%d")
                invoice.totalAmount = float(str(row[2]))

                customer = CustomerModel()
                customer.id =str(row[3])
                customer.identification = str(row[4])
                customer.name = str(row[5])

                invoice.customer = customer

        
            invoiceLine = self.__deserializeInvoiceLine(row)
            invoice.addLine(invoiceLine)

            invoiceDict[invoiceID] = invoice

        invoices = InvoiceModelCollection()
        for invoice in invoiceDict.values():
            invoices.add(invoice)

        return invoices
    

    def findAll(self) -> InvoiceModelCollection:
        sql = f"""SELECT invoice.id AS invoice_id, invoice.created_at AS invoice_created_at, invoice.total_amount AS invoice_total_amount,
        customers.id AS customer_id, customers.identification AS customer_identification, customers.name AS customer_name,
        invoice_line.id AS line_id, invoice_line.quantity AS line_quantity, invoice_line.total_amount AS line_total_amount, 
        products.id AS product_id, products.ica AS product_ica, products.name AS product_name, products.price AS product_price, 
        products.frecuency AS product_frecuency, products.type AS product_type,
        plague_control_products.grace_period AS product_grace_period, 
        fertilizer_control_products.last_application_date AS product_last_application_date, 
        antibiotic_products.dose AS product_dose, antibiotic_products.animal_type AS product_animal_type
        FROM invoice
        INNER JOIN customers ON customers.id = invoice.customer_id
        INNER JOIN invoice_line ON invoice.id = invoice_line.invoice_id
        INNER JOIN products ON products.id = invoice_line.product_id
        LEFT JOIN plague_control_products ON plague_control_products.id = products.id
        LEFT JOIN fertilizer_control_products ON fertilizer_control_products.id = products.id
        LEFT JOIN antibiotic_products ON antibiotic_products.id = products.id"""
        rows = self.mysqlProvider.fetch(sql)

        invoices = InvoiceModelCollection()
        invoiceDict: dict[str, InvoiceModel] = {}

        for row in rows:
            
            invoiceID = str(row[0])
            invoice: InvoiceModel

            if invoiceID in invoiceDict.keys():
                invoice = invoiceDict[invoiceID]
            else:
                invoice = InvoiceModel()
                invoice.id = invoiceID
                invoice.createdAt = datetime.strptime(str(row[1]), "%Y-%m-%d")
                invoice.totalAmount = float(str(row[2]))

                customer = CustomerModel()
                customer.id =str(row[3])
                customer.identification = str(row[4])
                customer.name = str(row[5])

                invoice.customer = customer

        
            invoiceLine = InvoiceLineModel()
            invoiceLine.id = str(row[6])
            invoiceLine.quantity = float(str(row[7]))
            invoiceLine.totalAmount = float(str(row[8]))
            
            product_type = str(row[14])
            product: ProductPlagueControlModel | ProductFertilizerControlModel | ProductAntibioticModel

            if product_type == PRODUCT_TYPE.PlageControl.name:
                product = ProductPlagueControlModel()
                product.id = str(row[9])
                product.ica = str(row[10])
                product.name = str(row[11])
                product.price = float(str(row[12]))
                product.frecuency = int(str(row[13]))
                product.type = PRODUCT_TYPE.PlageControl
                product.gracePeriod = int(str(15))
                

            if product_type == PRODUCT_TYPE.FertilizerControl.name:
                product = ProductFertilizerControlModel()
                product.id = str(row[9])
                product.ica = str(row[10])
                product.name = str(row[11])
                product.price = float(str(row[12]))
                product.frecuency = int(str(row[13]))
                product.type = PRODUCT_TYPE.PlageControl
                product.lastApplicationDate = datetime.strptime(str(row[16]), "%Y-%m-%d")

            if product_type == PRODUCT_TYPE.Antibiotic.name:
                product = ProductAntibioticModel()
                product.id = str(row[9])
                product.ica = str(row[10])
                product.name = str(row[11])
                product.price = float(str(row[12]))
                product.frecuency = int(str(row[13]))
                product.type = PRODUCT_TYPE.PlageControl
                product.dose = int(str(17))
                product.animalType = ANIMAL_TYPE_DICT[str(row[18])]

            invoiceLine.product = product
            invoice.addLine(invoiceLine)

        return invoices
    

    def __deserializeInvoice(self, rows) -> InvoiceModel:
        
        row = rows[0]
        
        invoice = InvoiceModel()

        invoice.id = str(row[0])
        invoice.createdAt = datetime.strptime(str(row[1]), "%Y-%m-%d")
        invoice.totalAmount = 0

        customer = CustomerModel()
        customer.id =str(row[3])
        customer.identification = str(row[4])
        customer.name = str(row[5])

        invoice.customer = customer

        for row in rows:
            invoiceLine = self.__deserializeInvoiceLine(row)
            invoice.addLine(invoiceLine)

        return invoice
    

    def __deserializeInvoiceLine(self, row) -> InvoiceLineModel:
        invoiceLine = InvoiceLineModel()
        invoiceLine.id = str(row[6])
        invoiceLine.quantity = float(str(row[7]))
        invoiceLine.totalAmount = 0
        
        product_type = str(row[14])
        product: ProductPlagueControlModel | ProductFertilizerControlModel | ProductAntibioticModel

        if product_type == PRODUCT_TYPE.PlageControl.name:
            product = ProductPlagueControlModel()
            product.id = str(row[9])
            product.ica = str(row[10])
            product.name = str(row[11])
            product.price = float(str(row[12]))
            product.frecuency = int(str(row[13]))
            product.type = PRODUCT_TYPE.PlageControl
            product.gracePeriod = int(str(15))
            

        if product_type == PRODUCT_TYPE.FertilizerControl.name:
            product = ProductFertilizerControlModel()
            product.id = str(row[9])
            product.ica = str(row[10])
            product.name = str(row[11])
            product.price = float(str(row[12]))
            product.frecuency = int(str(row[13]))
            product.type = PRODUCT_TYPE.PlageControl
            product.lastApplicationDate = datetime.strptime(str(row[16]), "%Y-%m-%d")

        if product_type == PRODUCT_TYPE.Antibiotic.name:
            product = ProductAntibioticModel()
            product.id = str(row[9])
            product.ica = str(row[10])
            product.name = str(row[11])
            product.price = float(str(row[12]))
            product.frecuency = int(str(row[13]))
            product.type = PRODUCT_TYPE.PlageControl
            product.dose = int(str(17))
            product.animalType = ANIMAL_TYPE_DICT[str(row[18])]

        invoiceLine.setProduct(product)
        return invoiceLine