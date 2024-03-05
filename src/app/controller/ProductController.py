from PyQt5.QtWidgets import QDialog
from src.app.model.product.ProductModel import ProductModel, ProductAntibioticModel, ProductFertilizerControlModel, ProductPlagueControlModel, PRODUCT_TYPE
from src.app.model.product.ProductModelCollection import ProductModelCollection
from src.app.model.product.ProductRepository import ProductRepository
from src.app.view.WIN_Product import WIN_Product
from uuid import uuid4

class ProductController:

    def __init__(self, productRepository: ProductRepository, view: WIN_Product):
        
        self.productRepository = productRepository
        self._view = view

        self._view.onProductCreate.connect(self._createProduct)
        self._view.onProductUpdate.connect(self._updateProduct)
        self._view.onProductDelete.connect(self._deleteProduct)
        self._view.onProductSelect.connect(self._selectProduct)
        self._view.connectEvents()

        self.products = ProductModelCollection()
        

    def _selectProduct(self, index: int): 
        product: ProductModel | None = self.products.select(index)

        if product == None:
            return
        
        self._view.selectProduct(product)


    def _createProduct(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):        
       
        if product.id == "":
            product.id = str(uuid4())

        self.productRepository.create(product)
        self.products = self.productRepository.findAll()
        self._view.refreshProducts(self.products)

        print(f"saved customer {product}")


    def _deleteProduct(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        self.productRepository.delete(product)
        
        self.products = self.productRepository.findAll()
        self._view.refreshProducts(self.products)

        print(f"deleted customer {product}")


    def _updateProduct(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        self.productRepository.update(product)
        
        self.customers = self.productRepository.findAll()
        self._view.refreshProducts(self.customers)
        self._view.selectProduct(product)

        print(f"updated customer {product}")


    def init(self):
        self.products = self.productRepository.findAll()
        self._view.refreshProducts(self.products)

        firstProduct: ProductModel | None = self.products.select(0)

        if firstProduct != None:
            self._view.selectProduct(firstProduct)
            
        self._view.show()
