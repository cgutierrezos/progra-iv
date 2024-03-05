from faker import Faker
from uuid import uuid4

from src.app.model.customer.CustomerModel import CustomerModel
from src.app.model.customer.CustomerModelCollection import CustomerModelCollection


class CustomerModelFactory:

    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def build(self) -> CustomerModel:  
        
        customer = CustomerModel()
        customer.id = str(uuid4())
        customer.identification = str(self.faker.random_int(10000000, 9999999999))
        customer.name = self.faker.name()

        return customer
    
    def buildMany(self, num: int) -> CustomerModelCollection:

        customers = CustomerModelCollection()

        for i in range(num):
            customers.add(self.build())

        return customers