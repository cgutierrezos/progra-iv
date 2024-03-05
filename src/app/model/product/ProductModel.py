from datetime import date
from enum import Enum
from abc import ABC, abstractmethod


PRODUCT_TYPE = Enum("PRODUCT_TYPE", ["PlageControl", "FertilizerControl", "Antibiotic"])
ANIMAL_TYPE = Enum("ANIMAL_TYPE", ["Bovino", "Caprino", "Porcino"])
ANIMAL_TYPE_DICT = {ANIMAL_TYPE.Bovino.name: ANIMAL_TYPE.Bovino, ANIMAL_TYPE.Caprino.name: ANIMAL_TYPE.Caprino, ANIMAL_TYPE.Porcino.name: ANIMAL_TYPE.Porcino}

class ProductModel(ABC):
    
    

    def __init__(self) -> None:
        self.id: str = ""
        self.ica: str = ""
        self.name: str = ""
        self.frecuency: int = 0
        self.price: float = 0
        self.type: PRODUCT_TYPE = PRODUCT_TYPE.PlageControl

    @abstractmethod
    def acceptCreation(self, repository):
        pass

    def __str__(self) -> str:
        return f"Product(id:{self.id},  ICA:{self.ica},  name:{self.name}, frecuency:{self.frecuency},  price:{self.price}, type:{self.type})"



class ProductPlagueControlModel(ProductModel):


    def __init__(self) -> None:
        super().__init__()
        self.gracePeriod: int = 0

    def __str__(self) -> str:
        baseStr: str = super().__str__()
        return baseStr.replace(")", f", gracePeriod:{self.gracePeriod})")
    
    def acceptCreation(self, repository):
        repository.acceptCreateFertilizerControl(self)
    

class ProductFertilizerControlModel(ProductModel):
    

    def __init__(self) -> None:
        super().__init__()
        self.lastApplicationDate: date = date.today()

    def __str__(self) -> str:
        baseStr: str = super().__str__()
        return baseStr.replace(")", f", lastApplicationDate:{self.lastApplicationDate})")
    
    def acceptCreation(self, repository):
        repository.acceptCreatePlagueControl(self)
    

class ProductAntibioticModel(ProductModel):


    def __init__(self) -> None:
        super().__init__()
        self.dose: int = 0
        self.animalType: ANIMAL_TYPE = ANIMAL_TYPE.Bovino

    def __str__(self) -> str:
        baseStr: str = super().__str__()
        return baseStr.replace(")", f", dose:{self.dose},   animalType:{self.animalType.value})")
    
    def acceptCreation(self, repository):
        repository.acceptCreateAntibiotic(self)


class ProductNoneModel(ProductModel):
    pass

    def acceptCreation(self, repository):
            pass