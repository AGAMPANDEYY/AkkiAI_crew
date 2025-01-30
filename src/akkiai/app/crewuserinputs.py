from pydantic import BaseModel
from typing import ClassVar

class SharedRunInputs:
    
    #storage for sharing inputs 
    _shared_instance=None

    def __init__(self):
        self.MODEL_NAME = ''
        self.PROMPT_CACHING=''
        self.INPUT_1=''

    @classmethod
    def set_shared_instance(cls, model_name: str,prompt_cache: str, user_input:str):
        if cls._shared_instance is None:
            cls._shared_instance=cls()
        cls._shared_instance.MODEL_NAME = model_name
        cls._shared_instance.PROMPT_CACHING = prompt_cache
        cls._shared_instance.INPUT_1 = user_input

    @classmethod
    def get_shared_instance(cls):
        if cls._shared_instance is None:
            cls._shared_instance = cls()
        return cls._shared_instance
