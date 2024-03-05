import unittest
from uuid import uuid4
from faker import Faker
from environment import Environment, FakeEnvironment
from src.app.model.invoice.InvoiceRepository import InvoiceRepository, MySQLInvoiceRepository
from src.app.model.product.ProductModel import ProductModel, ProductAntibioticModel, ProductFertilizerControlModel, ProductPlagueControlModel, PRODUCT_TYPE
from src.app.model.product.ProductRepository import ProductRepository, MySQLProductRepository
from src.providers.MySQLProvider import MySQLProvider
from typing import cast

from test.app.model.invoice.InvoiceModelFactory import InvoiceModelFactory



class TestInvoiceRepository(unittest.TestCase):
        

    @classmethod
    def setUpClass(cls):
        # Se ejecuta una vez antes de todas las pruebas
        cls.faker: Faker = Faker()
        cls.env: Environment = FakeEnvironment({"MYSQL_HOST": "localhost", "MYSQL_PORT": "3306", "MYSQL_DB": "test_progra4", "MYSQL_USER": "test_progra4", "MYSQL_PASS": ""})
        cls.mysqlProvider = MySQLProvider(cls.env)
        cls.mysqlProvider.connect()
        cls.invoiceRepository: InvoiceRepository = MySQLInvoiceRepository(cls.mysqlProvider)
        cls.invoiceFactory = InvoiceModelFactory(cls.faker)


    def setUp(self):

        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.mysqlProvider.execute("TRUNCATE TABLE antibiotic_products")
        self.mysqlProvider.execute("TRUNCATE TABLE products")
        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        # Se ejecuta una vez después de todas las pruebas
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        cls.mysqlProvider.execute("TRUNCATE TABLE antibiotic_products")
        cls.mysqlProvider.execute("TRUNCATE TABLE products")
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        cls.mysqlProvider.disconnect()
    
    @unittest.skip("not yet implement")
    def test_create_antibiotic_product(self):
        """
        Test that it can insert a product id mysql db
        """

        invoice = self.invoiceFactory.build()
        

        # self.ProductRepository.create(product)

        # productCreated: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel | None = self.ProductRepository.findOneByID(product.id)

        # if productCreated == None:
        #     self.fail(f"product id:{product.id} must be found")


        # self.assertEqual(product.id, productCreated.id)
        # self.assertEqual(product.name, productCreated.name)
        # self.assertEqual(product.ica, productCreated.ica)
        # self.assertEqual(product.frecuency, productCreated.frecuency)
        # self.assertEqual(product.price, productCreated.price)
        # self.assertEqual(product.type, productCreated.type)

        # self.assertIsInstance(productCreated, ProductAntibioticModel)

        # if issubclass(productCreated.__class__, ProductAntibioticModel):
        #     productCreated = cast(ProductAntibioticModel, productCreated)
        #     self.assertEqual(product.dose, productCreated.dose)
        #     self.assertEqual(product.animalType, productCreated.animalType)
            
            
        
        


    @unittest.skip("not yet implement")
    def test_update_product(self):
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
    def test_delete_product(self):
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
    def test_create_many_products(self):
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

        