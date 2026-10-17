# product.py - same as Product.java (the remote interface)
from abc import ABC, abstractmethod


# Lists the methods a product must have (like a Java interface)
class Product(ABC):
    @abstractmethod
    def get_name(self): pass

    @abstractmethod
    def get_price(self): pass

    @abstractmethod
    def get_description(self): pass
