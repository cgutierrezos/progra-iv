from typing import Callable
from src.app.model.product.ProductModel import ProductModel


class ProductModelCollection:
    

    def __init__(self) -> None:
        self._products: list[ProductModel] = list()

    def add(self, product: ProductModel):
        self._products.append(product)

    def update(self, productToUpdate: ProductModel):

        for product in self._products:
            if product.id == productToUpdate.id:
                product = productToUpdate
                return

    def delete(self, productToDelete: ProductModel):
        for product in self._products:
            if product.id == productToDelete.id:
                self._products.remove(product)
                return


    def forEach(self, eachProductCB: Callable[[ProductModel], None]):
        for product in self._products:
            eachProductCB(product)

    def count(self) -> int:
        return len(self._products)
    
    
    def findManyByFilter(self, filterCB: Callable[[ProductModel], bool]) -> 'ProductModelCollection':
        products = ProductModelCollection()
        for product in self._products:
            if filterCB(product):
                products.add(product)
        return products
    

    def findOneByFilter(self, filterCB: Callable[[ProductModel], bool]) -> ProductModel | None:
        for product in self._products:
            if filterCB(product):
                return product
        return None

    def findOneByID(self, id: str) -> ProductModel | None:
        return self.findOneByFilter(lambda product: product.id == id)

    
    def select(self, index: int) -> ProductModel | None:
        
        if index < self.count():
            return self._products[index]
        
        return None