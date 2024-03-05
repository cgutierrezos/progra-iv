from abc import ABC, abstractmethod
from src.app.model.customer.CustomerModel import CustomerModel
from src.app.model.customer.CustomerModelCollection import CustomerModelCollection
from src.providers.MySQLProvider import MySQLProvider


class CustomerRepository(ABC):


    @abstractmethod
    def create(self, customer: CustomerModel):
        pass
    
    @abstractmethod
    def update(self, customer: CustomerModel):
        pass

    @abstractmethod
    def delete(self, customer: CustomerModel):
        pass

    @abstractmethod
    def findOneByID(self,id: str) -> CustomerModel | None:
        pass

    @abstractmethod
    def findAll(self) -> CustomerModelCollection:
        pass

    @abstractmethod
    def findOneByIdentification(self, identification: str) -> CustomerModel | None:
        pass

    


class InMemoryCustomerRepository(CustomerRepository):
    
    def __init__(self) -> None:
        super().__init__()

        self.customers: dict[str, CustomerModel] = {}

    def create(self, customer: CustomerModel):
        self.customers[customer.id] = customer


    def update(self, customer: CustomerModel):
        self.customers[customer.id] = customer

    def delete(self, customer: CustomerModel):
        del self.customers[customer.id]


    def findOneByID(self, id: str) -> CustomerModel | None:
        return self.customers[id]

    
    def findAll(self) -> CustomerModelCollection:
        
        customers = list(self.customers.values())
        customerCollection = CustomerModelCollection()

        for customer in customers:
            customerCollection.add(customer)

        return customerCollection


    def findOneByIdentification(self, identification: str) -> CustomerModel | None:
        customers = list(self.customers.values())

        for customer in customers:
            if customer.identification == identification:
                return customer
            
        return None



class MySQLCustomerRepository(CustomerRepository):

    def __init__(self, mysqlProvider: MySQLProvider) -> None:
        super().__init__()

        self.mysqlProvider: MySQLProvider = mysqlProvider

    def create(self, customer: CustomerModel):
        
        sql = f"INSERT INTO customers (id, identification, name) VALUES ('{customer.id}', '{customer.identification}', '{customer.name}')"
        self.mysqlProvider.execute(sql)


    def update(self, customer: CustomerModel):
        
        sql = f"UPDATE customers SET identification = '{customer.identification}', name='{customer.name}' WHERE id = '{customer.id}' LIMIT 1"
        self.mysqlProvider.execute(sql)


    def delete(self, customer: CustomerModel):
        sql = f"DELETE FROM customers WHERE id = '{customer.id}' LIMIT 1"
        self.mysqlProvider.execute(sql)


    def findOneByID(self, id: str) -> CustomerModel | None:
        sql = f"SELECT id, name, identification FROM customers WHERE id='{id}' LIMIT 1"
        rows = self.mysqlProvider.fetch(sql)

        if len(rows) == 0:
            return None
        
        row = rows[0]

        customer = CustomerModel()

        customer.id = str(row[0])
        customer.name = str(row[1])
        customer.identification = str(row[2])

        return customer


    
    def findAll(self) -> CustomerModelCollection:
        
        sql = f"SELECT id, name, identification FROM customers"
        rows = self.mysqlProvider.fetch(sql)
        
        customers = CustomerModelCollection()

        for row in rows:
            customer = CustomerModel()

            customer.id = str(row[0])
            customer.name = str(row[1])
            customer.identification = str(row[2])
            customers.add(customer)

        return customers


    def findOneByIdentification(self, identification: str) -> CustomerModel | None:
        sql = f"SELECT id, name, identification FROM customers WHERE identification='{identification}' LIMIT 1"
        rows = self.mysqlProvider.fetch(sql)

        if len(rows) == 0:
            return None
        
        row = rows[0]

        customer = CustomerModel()

        customer.id = str(row[0])
        customer.name = str(row[1])
        customer.identification = str(row[2])

        return customer
