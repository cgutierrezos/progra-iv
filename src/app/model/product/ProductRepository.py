from abc import ABC, abstractmethod
from datetime import date, datetime
from src.app.model.product.ProductModelCollection import ProductModelCollection
from src.providers.MySQLProvider import MySQLProvider
from src.app.model.product.ProductModel import ANIMAL_TYPE_DICT, ProductModel, ProductFertilizerControlModel, ProductAntibioticModel, ProductPlagueControlModel, PRODUCT_TYPE, ANIMAL_TYPE
from typing import cast



class ProductRepository(ABC):

    @abstractmethod
    def create(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        pass
    
    @abstractmethod
    def update(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        pass

    @abstractmethod
    def delete(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        pass

    @abstractmethod
    def findOneByID(self,id: str) -> ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel | None:
        pass

    @abstractmethod
    def findAll(self) -> ProductModelCollection:
        pass

    


class InMemoryProductRepository(ProductRepository):
    
    

    def __init__(self) -> None:
        super().__init__()
        
        self.products: dict[str, ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel] = {}

    def create(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        self.products[product.id] = product


    def update(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        self.products[product.id] = product

    def delete(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        del self.products[product.id]


    def findOneByID(self, id: str) -> ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel | None:
        return self.products.get(id)

    
    def findAll(self) -> ProductModelCollection:
        
        products = list(self.products.values())
        productCollection = ProductModelCollection()

        for product in products:
            productCollection.add(product)

        return productCollection


    



class MySQLProductRepository(ProductRepository):

    

    def __init__(self, mysqlProvider: MySQLProvider) -> None:
        super().__init__()

        self.mysqlProvider: MySQLProvider = mysqlProvider

    def create(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        sql = f"INSERT INTO products (id, ica, name, frecuency, price, type) VALUES ('{product.id}', '{product.ica}', '{product.name}', {product.frecuency}, {product.price}, '{product.type.name}')"
        self.mysqlProvider.execute(sql)

        if issubclass(product.__class__, ProductAntibioticModel):
            product = cast(ProductAntibioticModel, product)
            sql = f"INSERT INTO antibiotic_products (id, product_id, dose, animal_type) VALUES ('{product.id}', '{product.id}', '{product.dose}', '{product.animalType.name}')"
            self.mysqlProvider.execute(sql)

        if issubclass(product.__class__, ProductPlagueControlModel):
            product = cast(ProductPlagueControlModel, product)
            sql = f"INSERT INTO plague_control_products (id, product_id, grace_period) VALUES ('{product.id}', '{product.id}', '{product.gracePeriod}')"
            self.mysqlProvider.execute(sql)

        if issubclass(product.__class__, ProductFertilizerControlModel):
            product = cast(ProductFertilizerControlModel, product)
            sql = f"INSERT INTO fertilizer_control_products (id, product_id, last_application_date) VALUES ('{product.id}', '{product.id}', '{product.lastApplicationDate.strftime('%Y-%m-%d')}')"
            self.mysqlProvider.execute(sql)


    def update(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        sql = f"UPDATE products SET ica = '{product.ica}', name='{product.name}', frecuency={product.frecuency}, price={product.price}  WHERE id = '{product.id}' LIMIT 1"
        self.mysqlProvider.execute(sql)

        if issubclass(product.__class__, ProductAntibioticModel):
            product = cast(ProductAntibioticModel, product)
            sql = f"UPDATE antibiotic_products SET dose={product.dose}, animal_type='{product.animalType.name}'"
            self.mysqlProvider.execute(sql)

        if issubclass(product.__class__, ProductPlagueControlModel):
            product = cast(ProductPlagueControlModel, product)
            sql = f"UPDATE plague_control_products SET grace_period={product.gracePeriod} WHERE id='{product.id}'"
            self.mysqlProvider.execute(sql)

        if issubclass(product.__class__, ProductFertilizerControlModel):
            product = cast(ProductFertilizerControlModel, product)
            sql = f"UPDATE fertilizer_control_products SET last_application_date='{product.lastApplicationDate.strftime('%Y-%m-%d')}' WHERE id='{product.id}'"
            self.mysqlProvider.execute(sql)


    def delete(self, product: ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel):
        sql = f"DELETE FROM products WHERE id = '{product.id}' LIMIT 1"
        self.mysqlProvider.execute(sql)


    def findOneByID(self, id: str) -> ProductAntibioticModel | ProductFertilizerControlModel | ProductPlagueControlModel | None:
        sql = f"SELECT id, ica, name, frecuency, price, type FROM products WHERE id='{id}' LIMIT 1"
        rows = self.mysqlProvider.fetch(sql)

        if len(rows) == 0:
            return None
        
        row = rows[0]

        type = str(row[5])

        # "PRODUCT_TYPE", ["PlageControl", "FertilizerControl", "Antibiotic"]
        if type == "PlageControl":
            product = ProductPlagueControlModel()

            product.id = str(row[0])
            product.ica = str(row[1])
            product.name = str(row[2])
            product.frecuency = int(str(row[3]))
            product.price = float(str(row[4]))
            product.type = PRODUCT_TYPE.PlageControl
            return self.__findOnePlageControl(product)
            

        if type == "FertilizerControl":
            product = ProductFertilizerControlModel()

            product.id = str(row[0])
            product.ica = str(row[1])
            product.name = str(row[2])
            product.frecuency = int(str(row[3]))
            product.price = float(str(row[4]))
            product.type = PRODUCT_TYPE.FertilizerControl
            return self.__findOneFertilizerControl(product)
            

        
        if type == "Antibiotic":
            product = ProductAntibioticModel()

            product.id = str(row[0])
            product.ica = str(row[1])
            product.name = str(row[2])
            product.frecuency = int(str(row[3]))
            product.price = float(str(row[4]))
            product.type = PRODUCT_TYPE.Antibiotic
            product.dose = 10
            product.animalType = ANIMAL_TYPE.Bovino

            return self.__findOneAntibiotic(product)
        
        return None


    
    def findAll(self) -> ProductModelCollection:
        
        sql = f"SELECT id, ica, name, frecuency, price, type FROM products"
        rows = self.mysqlProvider.fetch(sql)
        
        products = ProductModelCollection()

        for row in rows:

            type = str(row[5])

            # "PRODUCT_TYPE", ["PlageControl", "FertilizerControl", "Antibiotic"]
            if type == "PlageControl":
                product = ProductPlagueControlModel()

                product.id = str(row[0])
                product.ica = str(row[1])
                product.name = str(row[2])
                product.frecuency = int(str(row[3]))
                product.price = float(str(row[4]))
                product.type = PRODUCT_TYPE.PlageControl
                products.add(self.__findOnePlageControl(product))
                

            if type == "FertilizerControl":
                product = ProductFertilizerControlModel()

                product.id = str(row[0])
                product.ica = str(row[1])
                product.name = str(row[2])
                product.frecuency = int(str(row[3]))
                product.price = float(str(row[4]))
                product.type = PRODUCT_TYPE.FertilizerControl
                products.add(self.__findOneFertilizerControl(product))
                

            
            if type == "Antibiotic":
                product = ProductAntibioticModel()

                product.id = str(row[0])
                product.ica = str(row[1])
                product.name = str(row[2])
                product.frecuency = int(str(row[3]))
                product.price = float(str(row[4]))
                product.type = PRODUCT_TYPE.Antibiotic
                product.dose = 10
                product.animalType = ANIMAL_TYPE.Bovino

                products.add(self.__findOneAntibiotic(product))

        return products


    def __findOnePlageControl(self, product: ProductPlagueControlModel) -> ProductPlagueControlModel:
        sql = f"SELECT id, grace_period FROM plague_control_products WHERE id='{product.id}' LIMIT 1"
        rows = self.mysqlProvider.fetch(sql)

        if len(rows) == 0:
            raise Exception(f"Product Control Plague id:{product.id} not found")
        
        row = rows[0]

        product.gracePeriod  = int(str(row[1]))

        return product



    def __findOneFertilizerControl(self, product: ProductFertilizerControlModel) -> ProductFertilizerControlModel:
        sql = f"SELECT id, last_application_date FROM fertilizer_control_products WHERE id='{product.id}' LIMIT 1"
        rows = self.mysqlProvider.fetch(sql)

        if len(rows) == 0:
            raise Exception(f"Product Control Fertilizer id:{product.id} not found")
        
        row = rows[0]

        product.lastApplicationDate = datetime.strptime(str(row[1]), '%Y-%m-%d')

        return product

    def __findOneAntibiotic(self, product: ProductAntibioticModel) -> ProductAntibioticModel :
        sql = f"SELECT id, animal_type, dose FROM antibiotic_products WHERE id='{product.id}' LIMIT 1"
        rows = self.mysqlProvider.fetch(sql)

        if len(rows) == 0:
            raise Exception(f"Product Antibiotic id:{product.id} not found")
        
        row = rows[0]
        product.animalType = ANIMAL_TYPE_DICT[str(row[1])]
        product.dose = int(str(row[2]))

        return product