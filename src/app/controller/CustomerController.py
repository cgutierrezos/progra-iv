from PyQt5.QtWidgets import QDialog
from src.app.model.customer.CustomerModel import CustomerModel
from src.app.model.customer.CustomerModelCollection import CustomerModelCollection
from src.app.model.customer.CustomerRepository import CustomerRepository
from src.app.view.WIN_Customer import WIN_Customer
from uuid import uuid4

class CustomerController:

    def __init__(self, customerRepository: CustomerRepository, view: WIN_Customer):
        
        self.customerRepository = customerRepository
        self._view = view

        self._view.onCustomerCreate.connect(self._createCustomer)
        self._view.onCustomerUpdate.connect(self._updateCustomer)
        self._view.onCustomerDelete.connect(self._deleteCustomer)
        self._view.onCustomerSelect.connect(self._selectCustomer)
        self._view.connectEvents()

        self.customers = CustomerModelCollection()
        

    def _selectCustomer(self, index: int): 
        customer: CustomerModel | None = self.customers.select(index)

        if customer == None:
            return
        
        self._view.selectCustomer(customer)


    def _createCustomer(self, customer: CustomerModel):        
       
        if customer.id == "":
            customer.id = str(uuid4())

        self.customerRepository.create(customer)
        self.customers = self.customerRepository.findAll()
        self._view.refreshCustomers(self.customers)

        print(f"saved customer {customer}")


    def _deleteCustomer(self, customer: CustomerModel):
        self.customerRepository.delete(customer)
        
        self.customers = self.customerRepository.findAll()
        self._view.refreshCustomers(self.customers)

        print(f"deleted customer {customer}")


    def _updateCustomer(self, customer: CustomerModel):
        self.customerRepository.update(customer)
        
        self.customers = self.customerRepository.findAll()
        self._view.refreshCustomers(self.customers)
        self._view.selectCustomer(customer)

        print(f"updated customer {customer}")


    def init(self):
        self.customers = self.customerRepository.findAll()
        self._view.refreshCustomers(self.customers)

        firstCustomer: CustomerModel | None = self.customers.select(0)

        if firstCustomer != None:
            self._view.selectCustomer(firstCustomer)
            
        self._view.show()
