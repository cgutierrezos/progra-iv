import unittest
from uuid import uuid4
from faker import Faker
from environment import Environment, FakeEnvironment
from src.app.model.customer.CustomerModel import CustomerModel
from src.app.model.customer.CustomerModelCollection import CustomerModelCollection
from src.app.model.customer.CustomerRepository import CustomerRepository, MySQLCustomerRepository
from src.providers.MySQLProvider import MySQLProvider




class TestMySQLProvider(unittest.TestCase):
        

    @classmethod
    def setUpClass(cls):
        # Se ejecuta una vez antes de todas las pruebas
        cls.faker: Faker = Faker()
        cls.env: Environment = FakeEnvironment({"MYSQL_HOST": "localhost", "MYSQL_PORT": "3306", "MYSQL_DB": "test_progra4", "MYSQL_USER": "test_progra4", "MYSQL_PASS": ""})
        cls.mysqlProvider = MySQLProvider(cls.env)
        cls.mysqlProvider.connect()
        cls.customerRepository: CustomerRepository = MySQLCustomerRepository(cls.mysqlProvider)


    def setUp(self):
        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.mysqlProvider.execute("TRUNCATE TABLE customers")
        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        # Se ejecuta una vez después de todas las pruebas
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        cls.mysqlProvider.execute("TRUNCATE TABLE customers")
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        cls.mysqlProvider.disconnect()
    

    def test_create_customer(self):
        """
        Test that it can insert a customer id mysql db
        """

        customer = CustomerModel()
        customer.id = str(uuid4())
        customer.name = str(self.faker.name())
        customer.identification = str(self.faker.random_int(1000000000, 9999999999))

        self.customerRepository.create(customer)

        customerCreated: CustomerModel | None = self.customerRepository.findOneByID(customer.id)

        if customerCreated == None:
            self.fail(f"Customer id:{customer.id} must be found")

        self.assertEqual(customer.id, customerCreated.id)
        self.assertEqual(customer.name, customerCreated.name)
        self.assertEqual(customer.identification, customerCreated.identification)


    def test_update_customer(self):
        """
        Test that it can UPDATE a customer id mysql db
        """

        customer = CustomerModel()
        customer.id = "1"
        customer.name = "cristian"
        customer.identification = "1088018783"

        self.customerRepository.create(customer)

        customerCreated: CustomerModel | None = self.customerRepository.findOneByID(customer.id)

        if customerCreated == None:
            self.fail(f"Customer id:{customer.id} must be found")

        self.assertEqual(customer.id, customerCreated.id)
        self.assertEqual(customer.name, customerCreated.name)
        self.assertEqual(customer.identification, customerCreated.identification)

        customerCreated.name = "alejandro"
        customerCreated.identification = "10000000"

        self.customerRepository.update(customerCreated)

        customerUpdated: CustomerModel | None = self.customerRepository.findOneByID(customerCreated.id)

        if customerUpdated == None:
            self.fail(f"Customer id:{customer.id} must be found")

        self.assertEqual(customerUpdated.id, customer.id)
        self.assertNotEqual(customerUpdated.name, customer.name)
        self.assertNotEqual(customerUpdated.identification, customer.identification)
        self.assertEqual(customerUpdated.id, customerCreated.id)
        self.assertEqual(customerUpdated.name, customerCreated.name)
        self.assertEqual(customerUpdated.identification, customerCreated.identification)


    def test_delete_customer(self):
        """
        Test that it can DELETE a customer id mysql db
        """

        customer = CustomerModel()
        customer.id = "1"
        customer.name = "cristian"
        customer.identification = "1088018783"

        self.customerRepository.create(customer)

        customerCreated: CustomerModel | None = self.customerRepository.findOneByID(customer.id)

        if customerCreated == None:
            self.fail(f"Customer id:{customer.id} must be found")

        self.assertEqual(customer.id, customerCreated.id)
        self.assertEqual(customer.name, customerCreated.name)
        self.assertEqual(customer.identification, customerCreated.identification)

        self.customerRepository.delete(customer)
       
        customerDeleted: CustomerModel | None = self.customerRepository.findOneByID(customer.id)

        self.assertIsNone(customerDeleted)

    
    def test_create_many_customers(self):
        """
        Test that it can insert a customer id mysql db
        """

        customers = CustomerModelCollection()
        for i in range(10):
            customer = CustomerModel()
            customer.id = str(uuid4())
            customer.name = str(self.faker.name())
            customer.identification = str(self.faker.random_int(1000000000, 9999999999))

            self.customerRepository.create(customer)

            customers.add(customer)
        

        customersCreated: CustomerModelCollection = self.customerRepository.findAll()

        def customersCB(customer: CustomerModel):
            customerCreated: CustomerModel | None = customersCreated.findOneByID(customer.id)

            if customerCreated == None:
                self.fail(f"Customer id:{customer.id} must be found")

            self.assertEqual(customer.id, customerCreated.id)
            self.assertEqual(customer.name, customerCreated.name)
            self.assertEqual(customer.identification, customerCreated.identification)

        customers.forEach(customersCB)

        