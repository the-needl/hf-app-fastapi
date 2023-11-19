from typing import Dict, List
from pydantic import BaseModel

import logging

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM
from transformers import pipeline

from app.core.config import settings
from app.models.base import Base
from app.models.instances import *

# from app.models.payload import SUMPayload
# from app.models.result import SUMResult
# from app.core.messages import NO_VALID_PAYLOAD

logger = logging.getLogger(__name__)

def create_instance(model_type: str) -> Base:
    try:
        module = importlib.import_module(f"app.models.instances.{model_type}")
        model_class = getattr(module, f"{model_type}Model")
    except ImportError:
        print(f"Module {model_type} not found.")
    except AttributeError:
        print(f"Class {model_type}Model not found.")
        
    return model()
    
class NERModel(Base):
    pass

class KEYModel(Base):
    pass

class QAModel(Base):
    pass