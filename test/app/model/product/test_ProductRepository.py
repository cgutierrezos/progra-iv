import unittest
from uuid import uuid4
from faker import Faker
from environment import Environment, FakeEnvironment
from src.app.model.product.ProductModel import ProductAntibioticModel, ProductFertilizerControlModel, ProductModel, ProductPlagueControlModel, PRODUCT_TYPE
from src.app.model.product.ProductRepository import ProductRepository, MySQLProductRepository
from src.providers.MySQLProvider import MySQLProvider
from typing import cast

from test.app.model.product.ProductModelFactory import ProductModelFactory



class TestProductRepository(unittest.TestCase):
        

    @classmethod
    def setUpClass(cls):
        # Se ejecuta una vez antes de todas las pruebas
        cls.faker: Faker = Faker()
        Faker.seed()
        cls.env: Environment = FakeEnvironment({"MYSQL_HOST": "localhost", "MYSQL_PORT": "3306", "MYSQL_DB": "test_progra4", "MYSQL_USER": "test_progra4", "MYSQL_PASS": ""})
        cls.mysqlProvider = MySQLProvider(cls.env)
        cls.mysqlProvider.connect()
        cls.ProductRepository: ProductRepository = MySQLProductRepository(cls.mysqlProvider)
        cls.productFactory = ProductModelFactory(cls.faker)


    def setUp(self):

        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.mysqlProvider.execute("TRUNCATE TABLE antibiotic_products")
        self.mysqlProvider.execute("TRUNCATE TABLE plague_control_products")
        self.mysqlProvider.execute("TRUNCATE TABLE fertilizer_control_products")
        self.mysqlProvider.execute("TRUNCATE TABLE products")
        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        # Se ejecuta una vez después de todas las pruebas
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        cls.mysqlProvider.execute("TRUNCATE TABLE antibiotic_products")
        cls.mysqlProvider.execute("TRUNCATE TABLE plague_control_products")
        cls.mysqlProvider.execute("TRUNCATE TABLE fertilizer_control_products")
        cls.mysqlProvider.execute("TRUNCATE TABLE products")
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        cls.mysqlProvider.disconnect()
    
    
    def test_create_antibiotic_product(self):
        """
        Test that it can insert a product id mysql db
        """

        product = self.productFactory.build()

        self.ProductRepository.create(product)

        productCreated: ProductModel | None = self.ProductRepository.findOneByID(product.id)

        if productCreated == None:
            self.fail(f"product id:{product.id} must be found")


        self.assertEqual(product.id, productCreated.id)
        self.assertEqual(product.name, productCreated.name)
        self.assertEqual(product.ica, productCreated.ica)
        self.assertEqual(product.frecuency, productCreated.frecuency)
        self.assertEqual(product.price, productCreated.price)
        self.assertEqual(product.type, productCreated.type)

        if issubclass(productCreated.__class__, ProductAntibioticModel):
            productCreated = cast(ProductAntibioticModel, productCreated)
            product = cast(ProductAntibioticModel, product)
            self.assertEqual(product.dose, productCreated.dose)
            self.assertEqual(product.animalType, productCreated.animalType)

        if issubclass(productCreated.__class__, ProductFertilizerControlModel):
            productCreated = cast(ProductFertilizerControlModel, productCreated)
            product = cast(ProductFertilizerControlModel, product)
            self.assertEqual(product.lastApplicationDate.strftime("%Y-$m-%d"), productCreated.lastApplicationDate.strftime("%Y-$m-%d"))
            
        
        if issubclass(productCreated.__class__, ProductPlagueControlModel):
            productCreated = cast(ProductPlagueControlModel, productCreated)
            product = cast(ProductPlagueControlModel, product)
            self.assertEqual(product.gracePeriod, productCreated.gracePeriod)
            
        
        


    def test_update_product(self):
        """
        Test that it can UPDATE a product id mysql db
        """

        product = self.productFactory.build()

        self.ProductRepository.create(product)

        productCreated: ProductModel | None = self.ProductRepository.findOneByID(product.id)

        if productCreated == None:
            self.fail(f"product id:{product.id} must be found")

        productCreated.name = str(self.faker.name())
        productCreated.ica = str(self.faker.random_int(1000000, 999999999))
        productCreated.price = float(self.faker.random_int(1000000, 999999999))

        self.ProductRepository.update(productCreated)

        productUpdated = self.ProductRepository.findOneByID(productCreated.id)

        if productUpdated == None:
            self.fail(f"product id:{product.id} must be found")

        self.assertEqual(productUpdated.id, productCreated.id)
        self.assertEqual(productUpdated.name, productCreated.name)
        self.assertEqual(productUpdated.ica, productCreated.ica)
        self.assertEqual(productUpdated.price, productCreated.price)
        self.assertEqual(productUpdated.frecuency, productCreated.frecuency)
        self.assertEqual(productUpdated.type, productCreated.type)

        if issubclass(productCreated.__class__, ProductAntibioticModel):
            productCreated = cast(ProductAntibioticModel, productCreated)
            productUpdated = cast(ProductAntibioticModel, productUpdated)
            self.assertEqual(productUpdated.dose, productCreated.dose)
            self.assertEqual(productUpdated.animalType, productCreated.animalType)

        if issubclass(productCreated.__class__, ProductFertilizerControlModel):
            productCreated = cast(ProductFertilizerControlModel, productCreated)
            productUpdated = cast(ProductFertilizerControlModel, productUpdated)
            self.assertEqual(productUpdated.lastApplicationDate.strftime("%Y-$m-%d"), productCreated.lastApplicationDate.strftime("%Y-$m-%d"))
            
        
        if issubclass(productCreated.__class__, ProductPlagueControlModel):
            productCreated = cast(ProductPlagueControlModel, productCreated)
            productUpdated = cast(ProductPlagueControlModel, productUpdated)
            self.assertEqual(productUpdated.gracePeriod, productCreated.gracePeriod)


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

        