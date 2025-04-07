from abc import ABC, abstractmethod

class Model(ABC):
    """Interface for language model implementations using Strategy pattern"""
    
    @abstractmethod
    def generate_content(self, contents):
        """Generate content based on the provided input"""
        pass