from pydantic import BaseModel
from typing import ClassVar

class SharedRunInputs:
    
    #storage for sharing inputs 
    _shared_instance=None

    def __init__(self):
        self.MODEL_NAME = ''

    @classmethod
    def set_shared_instance(cls, model_name: str):
        if cls._shared_instance is None:
            cls._shared_instance=cls()
        cls._shared_instance.MODEL_NAME = model_name

    @classmethod
    def get_shared_instance(cls):
        if cls._shared_instance is None:
            cls._shared_instance = cls()
        return cls._shared_instance
