from typing import Callable
from src.app.model.customer.CustomerModel import CustomerModel


class CustomerModelCollection:
    

    def __init__(self) -> None:
        self._customers: list[CustomerModel] = list()

    def add(self, customer: CustomerModel):
        self._customers.append(customer)

    def update(self, customerToUpdate: CustomerModel):

        for customer in self._customers:
            if customer.id == customerToUpdate.id:
                customer = customerToUpdate
                return

    def delete(self, customerToDelete: CustomerModel):
        for customer in self._customers:
            if customer.id == customerToDelete.id:
                self._customers.remove(customer)
                return


    def forEach(self, eachCustomerCB: Callable[[CustomerModel], None]):
        for customer in self._customers:
            eachCustomerCB(customer)

    def count(self) -> int:
        return len(self._customers)
    
    
    def findManyByFilter(self, filterCB: Callable[[CustomerModel], bool]) -> 'CustomerModelCollection':
        customers = CustomerModelCollection()
        for customer in self._customers:
            if filterCB(customer):
                customers.add(customer)
        return customers
    

    def findOneByFilter(self, filterCB: Callable[[CustomerModel], bool]) -> CustomerModel | None:
        for customer in self._customers:
            if filterCB(customer):
                return customer
        return None

    def findOneByID(self, id: str) -> CustomerModel | None:
        return self.findOneByFilter(lambda customer: customer.id == id)

    
    def select(self, index: int) -> CustomerModel | None:
        
        if index < self.count():
            return self._customers[index]
        
        return None