from typing import Dict, List
from pydantic import BaseModel

import logging

import importlib

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from app.models.base import Base
from app.models.instances import *

logger = logging.getLogger(__name__)

def create_instance(model_type: str) -> Base:
    try:
        module = importlib.import_module(f"app.models.instances.{model_type}")
        model_class = getattr(module, f"{model_type}Model")
    except ImportError:
        print(f"Module {model_type} not found.")
    except AttributeError:
        print(f"Class {model_type}Model not found.")
        
    return model_class()
    
class NERModel(Base):
    pass

class KEYModel(Base):
    pass

class QAModel(Base):
    pass