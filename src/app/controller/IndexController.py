from environment import Environment
from src.app.controller.ProductController import ProductController
from src.app.model.customer.CustomerRepository import CustomerRepository, MySQLCustomerRepository
from src.app.model.product.ProductRepository import MySQLProductRepository, ProductRepository
from src.app.view.WIN_Index import WIN_Index 
from src.app.view.WIN_Customer import WIN_Customer
from src.app.controller.CustomerController import CustomerController


from src.app.view.WIN_Product import WIN_Product
from src.providers.MySQLProvider import MySQLProvider


class IndexController:

    

    def __init__(self, env: Environment, view: WIN_Index):
        self._view = view
        
        self._view.openCustomer.connect(self.openCustomer)
        self._view.openProduct.connect(self.openProduct)
        self._view.openInvoice.connect(self.openInvoice)
        
        mysqlProvider = MySQLProvider(env)
        mysqlProvider.connect()

        self.customerRepository: CustomerRepository = MySQLCustomerRepository(mysqlProvider)
        self.winCustomer: WIN_Customer
        self.customerController: CustomerController

        self.productRepository: ProductRepository = MySQLProductRepository(mysqlProvider)
        self.winProduct: WIN_Product
        self.productController: ProductController

        self._view.connectEvents()


    def openCustomer(self):
        self.winCustomer = WIN_Customer(self._view)
        self.customerController = CustomerController(self.customerRepository, self.winCustomer)
        self.customerController.init()

    def openProduct(self):
        self.winProduct = WIN_Product(self._view)
        self.productController = ProductController(self.productRepository, self.winProduct)
        self.productController.init()

    def openInvoice(self):
        # self._modelo.modificar_cliente(cedula, nuevo_nombre)
        # self._view.mostrar_clientes(self._modelo.obtener_clientes())
        # self._view.mostrar_mensaje("Cliente modificado exitosamente.")
        pass


    def init(self):
        self._view.show()