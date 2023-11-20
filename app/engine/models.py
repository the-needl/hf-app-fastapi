from typing import Dict, List
from pydantic import BaseModel

import logging

import importlib

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from app.engine.base import Base
from app.engine.instances import *

logger = logging.getLogger(__name__)

def create_instance(model_type: str) -> Base:
    try:
        module = importlib.import_module(f"app.engine.instances.{model_type}")
        model_class = getattr(module, f"{model_type}Model")
    except ImportError:
        print(f"Module {model_type} not found.")
    except AttributeError:
        print(f"Class {model_type}Model not found.")
        
    return model_class()