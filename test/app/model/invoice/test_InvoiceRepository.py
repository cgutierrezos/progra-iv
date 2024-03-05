from datetime import datetime
import unittest
from uuid import uuid4
from faker import Faker
from environment import Environment, FakeEnvironment
from src.app.model.customer.CustomerModel import CustomerModel
from src.app.model.customer.CustomerModelCollection import CustomerModelCollection
from src.app.model.customer.CustomerRepository import CustomerRepository, MySQLCustomerRepository
from src.app.model.invoice.InvoiceModel import InvoiceLineModel, InvoiceModel
from src.app.model.invoice.InvoiceModelCollection import InvoiceModelCollection
from src.app.model.invoice.InvoiceRepository import InvoiceRepository, MySQLInvoiceRepository
from src.app.model.product.ProductModel import ProductModel, ProductAntibioticModel, ProductFertilizerControlModel, ProductPlagueControlModel, PRODUCT_TYPE
from src.app.model.product.ProductModelCollection import ProductModelCollection
from src.app.model.product.ProductRepository import ProductRepository, MySQLProductRepository
from src.providers.MySQLProvider import MySQLProvider
from typing import cast
from test.app.model.customer.CustomerModelFactory import CustomerModelFactory

from test.app.model.invoice.InvoiceModelFactory import InvoiceModelFactory
from test.app.model.product.ProductModelFactory import ProductModelFactory



class TestInvoiceRepository(unittest.TestCase):
        

    @classmethod
    def setUpClass(cls):
        # Se ejecuta una vez antes de todas las pruebas
        cls.faker: Faker = Faker()
        cls.env: Environment = FakeEnvironment({"MYSQL_HOST": "localhost", "MYSQL_PORT": "3306", "MYSQL_DB": "test_progra4", "MYSQL_USER": "test_progra4", "MYSQL_PASS": ""})
        cls.mysqlProvider = MySQLProvider(cls.env)
        cls.mysqlProvider.connect()
        cls.invoiceRepository: InvoiceRepository = MySQLInvoiceRepository(cls.mysqlProvider)
        cls.productRepository: ProductRepository = MySQLProductRepository(cls.mysqlProvider)
        cls.customerRepository: CustomerRepository = MySQLCustomerRepository(cls.mysqlProvider)
        
        cls.invoiceFactory = InvoiceModelFactory(cls.faker)
        cls.productFactory = ProductModelFactory(cls.faker)
        cls.customerFactory = CustomerModelFactory(cls.faker)


    def setUp(self):

        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.mysqlProvider.execute("TRUNCATE TABLE customers")
        self.mysqlProvider.execute("TRUNCATE TABLE antibiotic_products")
        self.mysqlProvider.execute("TRUNCATE TABLE plague_control_products")
        self.mysqlProvider.execute("TRUNCATE TABLE fertilizer_control_products")
        self.mysqlProvider.execute("TRUNCATE TABLE products")
        self.mysqlProvider.execute("TRUNCATE TABLE invoice_line")
        self.mysqlProvider.execute("TRUNCATE TABLE invoice")
        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        # Se ejecuta una vez después de todas las pruebas
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        cls.mysqlProvider.execute("TRUNCATE TABLE customers")
        cls.mysqlProvider.execute("TRUNCATE TABLE antibiotic_products")
        cls.mysqlProvider.execute("TRUNCATE TABLE plague_control_products")
        cls.mysqlProvider.execute("TRUNCATE TABLE fertilizer_control_products")
        cls.mysqlProvider.execute("TRUNCATE TABLE products")
        cls.mysqlProvider.execute("TRUNCATE TABLE invoice_line")
        cls.mysqlProvider.execute("TRUNCATE TABLE invoice")
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        cls.mysqlProvider.disconnect()
    

    def test_create_invoice(self):
        """
        Test that it can insert a product id mysql db
        """

        customer: CustomerModel = self.customerFactory.build()
        products: ProductModelCollection = self.productFactory.buildMany(3)

        self.customerRepository.create(customer)
        products.forEach(lambda product: self.productRepository.create(product))

        invoice: InvoiceModel = self.invoiceFactory.build()

        invoice.setCustomer(customer)
        invoice.createdAt = datetime.strptime(str(self.faker.date()), "%Y-%m-%d")

        def addToInvoice(product: ProductModel):
            invoiceLine = InvoiceLineModel()
            invoiceLine.id = str(uuid4())
            invoiceLine.quantity = int(self.faker.random_int(1, 5))
            invoiceLine.setProduct(product)
            invoice.addLine(invoiceLine)

        products.forEach(addToInvoice)

        self.invoiceRepository.create(invoice)

        invoiceCreated: InvoiceModel = self.invoiceRepository.findOneByID(invoice.id)

        if invoiceCreated == None:
            self.fail(f"Invoice id:{invoice.id} must be found")
        
        self.assertEqual(invoice.id, invoiceCreated.id)
        self.assertEqual(invoice.createdAt, invoiceCreated.createdAt)
        self.assertEqual(invoice.totalAmount, invoiceCreated.totalAmount)
        self.assertEqual(invoice.customer.id, invoiceCreated.customer.id)
        self.assertEqual(invoice.customer.name, invoiceCreated.customer.name)
        self.assertEqual(invoice.customer.identification, invoiceCreated.customer.identification)

        # Check if lines are equals here
        


    def test_findInvoicesByCustomerIdentification(self):
        """
        Test that it can insert a product id mysql db
        """

        customers: CustomerModelCollection = self.customerFactory.buildMany(2)
        
        customer1 = customers.get(0)
        customer2 = customers.get(1)
        
        if customer1 == None:
            self.fail("Customer1 must be found")

        if customer2 == None:
            self.fail("Customer2 must be found")

        products: ProductModelCollection = self.productFactory.buildMany(self.faker.random_int(1, 5))
        

        customers.forEach(lambda customer: self.customerRepository.create(customer))
        products.forEach(lambda product: self.productRepository.create(product))

        invoices_customer1_count = self.faker.random_int(1, 3)
        invoices_customer1: InvoiceModelCollection = self.invoiceFactory.buildMany(invoices_customer1_count)

        def createInvoiceForCustomer1(invoice: InvoiceModel):
           
            invoice.setCustomer(customer1)
            invoice.createdAt = datetime.strptime(str(self.faker.date()), "%Y-%m-%d")

            def addToInvoice(product: ProductModel):
                invoiceLine = InvoiceLineModel()
                invoiceLine.id = str(uuid4())
                invoiceLine.quantity = int(self.faker.random_int(1, 5))
                invoiceLine.setProduct(product)
                invoice.addLine(invoiceLine)

            products.forEach(addToInvoice)

            self.invoiceRepository.create(invoice)
        
        invoices_customer1.forEach(createInvoiceForCustomer1)

        if invoices_customer1.count() == 0:
            self.fail("Invoices for customer 1 must be greather than 0")

        invoicesForCustomer1Found: InvoiceModelCollection = self.invoiceRepository.findManyByCustomerIdentification(customer1.identification)
        invoicesForCustomer2Found: InvoiceModelCollection = self.invoiceRepository.findManyByCustomerIdentification(customer2.identification)

        self.assertEqual(invoicesForCustomer1Found.count(), invoices_customer1.count())
        self.assertEqual(invoicesForCustomer2Found.count(), 0)
        


    @unittest.skip("not yet implement")
    def test_update_invoice(self):
        """
        Test that it can UPDATE a product id mysql db
        """

        # product = ProductModel()
        # product.id = "1"
        # product.name = "cristian"
        # product.identification = "1088018783"

        # self.ProductRepository.create(product)

        # productCreated: ProductModel | None = self.ProductRepository.findOneByID(product.id)

        # if productCreated == None:
        #     self.fail(f"product id:{product.id} must be found")

        # self.assertEqual(product.id, productCreated.id)
        # self.assertEqual(product.name, productCreated.name)
        # self.assertEqual(product.identification, productCreated.identification)

        # productCreated.name = "alejandro"
        # productCreated.identification = "10000000"

        # self.ProductRepository.update(productCreated)

        # productUpdated: ProductModel | None = self.ProductRepository.findOneByID(productCreated.id)

        # if productUpdated == None:
        #     self.fail(f"product id:{product.id} must be found")

        # self.assertEqual(productUpdated.id, product.id)
        # self.assertNotEqual(productUpdated.name, product.name)
        # self.assertNotEqual(productUpdated.identification, product.identification)
        # self.assertEqual(productUpdated.id, productCreated.id)
        # self.assertEqual(productUpdated.name, productCreated.name)
        # self.assertEqual(productUpdated.identification, productCreated.identification)


    @unittest.skip("not yet implement")
    def test_delete_invoice(self):
        """
        Test that it can DELETE a product id mysql db
        """

        # product = ProductModel()
        # product.id = "1"
        # product.name = "cristian"
        # product.identification = "1088018783"

        # self.ProductRepository.create(product)

        # productCreated: ProductModel | None = self.ProductRepository.findOneByID(product.id)

        # if productCreated == None:
        #     self.fail(f"product id:{product.id} must be found")

        # self.assertEqual(product.id, productCreated.id)
        # self.assertEqual(product.name, productCreated.name)
        # self.assertEqual(product.identification, productCreated.identification)

        # self.ProductRepository.delete(product)
       
        # productDeleted: ProductModel | None = self.ProductRepository.findOneByID(product.id)

        # self.assertIsNone(productDeleted)

    
    @unittest.skip("not yet implement")
    def test_create_many_invoices(self):
        """
        Test that it can insert a product id mysql db
        """

        # products = ProductModelCollection()
        # for i in range(10):
        #     product = ProductModel()
        #     product.id = str(uuid4())
        #     product.name = str(self.faker.name())
        #     product.identification = str(self.faker.random_int(1000000000, 9999999999))

        #     self.ProductRepository.create(product)

        #     products.add(product)
        

        # productsCreated: ProductModelCollection = self.ProductRepository.findAll()

        # def productsCB(product: ProductModel):
        #     productCreated: ProductModel | None = productsCreated.findOneByID(product.id)

        #     if productCreated == None:
        #         self.fail(f"product id:{product.id} must be found")

        #     self.assertEqual(product.id, productCreated.id)
        #     self.assertEqual(product.name, productCreated.name)
        #     self.assertEqual(product.identification, productCreated.identification)

        # products.forEach(productsCB)

        