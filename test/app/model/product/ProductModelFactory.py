from faker import Faker
from uuid import uuid4

from src.app.model.product.ProductModel import ANIMAL_TYPE, PRODUCT_TYPE, ProductAntibioticModel, ProductFertilizerControlModel, ProductPlagueControlModel
from src.app.model.product.ProductModelCollection import ProductModelCollection


class ProductModelFactory:

    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def build(self) -> ProductPlagueControlModel | ProductFertilizerControlModel | ProductAntibioticModel:
        
        product_type_id = self.faker.random_int(1, 3)
        product: ProductPlagueControlModel | ProductFertilizerControlModel | ProductAntibioticModel

        if product_type_id == 1:
            product = ProductPlagueControlModel()
            product.id = str(uuid4())
            product.ica = str(self.faker.random_int(100000000, 9999999999999))
            product.name = str(self.faker.name())
            product.price = float(str(self.faker.random_int(10, 50)))
            product.frecuency = int(str(self.faker.random_int(10, 50)))
            product.type = PRODUCT_TYPE.PlageControl
            product.gracePeriod = int(str(15))
            

        if product_type_id == 2:
            product = ProductFertilizerControlModel()
            product.id = str(uuid4())
            product.ica = str(self.faker.random_int(100000000, 9999999999999))
            product.name = str(self.faker.name())
            product.price = float(str(self.faker.random_int(10, 50)))
            product.frecuency = int(str(self.faker.random_int(10, 50)))
            product.type = PRODUCT_TYPE.PlageControl
            product.lastApplicationDate = self.faker.date()

        if product_type_id == PRODUCT_TYPE.Antibiotic.name:
            product = ProductAntibioticModel()
            product.id = str(uuid4())
            product.ica = str(self.faker.random_int(100000000, 9999999999999))
            product.name = str(self.faker.name())
            product.price = float(str(self.faker.random_int(10, 50)))
            product.frecuency = int(str(self.faker.random_int(10, 50)))
            product.type = PRODUCT_TYPE.PlageControl
            product.dose = int(self.faker.random_int(10, 50))
            product.animalType = ANIMAL_TYPE.Bovino

        return product
    
    def buildMany(self, num: int) -> ProductModelCollection:

        products = ProductModelCollection()
        for i in range(num):
             products.add(self.build())

        return products