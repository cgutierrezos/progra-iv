import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

class Environment(ABC):
    
    @abstractmethod
    def get(self, key: str, default: str) -> str:
        pass
    
    @abstractmethod
    def getOrFails(self, key: str) -> str:
        pass
    

class DotEnvEnvironment(Environment):

    def __init__(self, dotenv_path: str) -> None:
        super().__init__()
        self.dotenv_path = dotenv_path
    
    def load(self):
        load_dotenv(self.dotenv_path)

    def get(self, key: str, default: str) -> str:
        value = os.getenv(key)
        
        if value == None:
            return default
        
        return value
    
    def getOrFails(self, key: str) -> str:
        value = os.getenv(key)
        
        if value == None:
            raise Exception(f"Environment {key} not found")
        
        return value
    
    
class FakeEnvironment(Environment):

    def __init__(self, env: dict[str, str]) -> None:
        super().__init__()
        self.env = env

    def get(self, key: str, default: str) -> str:
        value = self.env.get(key)
        
        if value == None:
            return default
        
        return value
    
    def getOrFails(self, key: str) -> str:
        value = self.env.get(key)
        
        if value == None:
            raise Exception(f"Environment {key} not found")
        
        return value
