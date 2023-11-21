from typing import List, Tuple

from pathlib import Path

import logging
from abc import abstractmethod
import importlib

import torch
from transformers import PreTrainedModel, PreTrainedTokenizer

from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

logger = logging.getLogger(__name__)

class Base:
    def __init__(self,
                 model_name: str,
                 model_path: str,
                 model_loader: PreTrainedModel,
                 tokenizer_loader: PreTrainedTokenizer):
        
        self.model_name = Path(model_name)
        self.model_path = Path(model_path)
        self.model_loader = model_loader
        self.tokenizer_loader = tokenizer_loader
        
        self.save_path = self.model_path / self.model_name
        
        if not self.save_path.exists():
            logger.debug(f"[+] {self.save_path} does not exit!")
            self.save_path.mkdir(parents=True, exist_ok=True)
            self.__download_model()
        else:
            logger.debug(f"[+] Model already existing, loading from {self.save_path}")

        self.tokenizer, self.model = self.__load_model()

    @abstractmethod
    def _pre_process(self):
        pass
    
    @abstractmethod
    def _post_process(self):
        pass
    
    @abstractmethod
    def _output(self):
        pass

    @abstractmethod
    def output(self):
        pass
    
    def _get_context_len(self, context: str) -> int:
        """
        Return context token length.
        """
        context_len = len(self.tokenizer.encode(context))
        # logger.debug(f"[-] Context length: {context_len}")
        print(f"[-] Context length: {context_len}")
        
        return context_len
    
    def _split_context(self,
                       context: str,
                       chunk_length: int = None) -> List:
        """
        Return context as list of chunks only if len(context) <= len(chunk).
        """
        if not chunk_length:
            chunk_length = self.tokenizer.model_max_length
            
        # logger.debug(f"[-] Max model token length: {chunk_length}")
        print(f"[-] Max model token length: {chunk_length}")
        
        if self._get_context_len(context) <= chunk_length:
            texts = [context]
        else:
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=chunk_length*0.9, chunk_overlap=chunk_length
                )
            texts = text_splitter.split_text(context)
            
        return texts
    
    def __repr__(self):
        return f"{self.__class__.__name__}(model={self.save_path})"

    # Download model from HuggingFace
    def __download_model(self) -> None:

        logger.debug(f"[+] Downloading {self.model_name}")
        tokenizer = self.tokenizer_loader.from_pretrained(f"{self.model_name}")
        model = self.model_loader.from_pretrained(f"{self.model_name}")

        logger.debug(f"[+] Saving {self.model_name} to {self.save_path}")
        tokenizer.save_pretrained(f"{self.save_path}")
        model.save_pretrained(f"{self.save_path}")

        logger.debug("[+] Process completed")

    # Load model
    def __load_model(self) -> Tuple:

        logger.debug(f"[+] Loading model from {self.save_path}")
        tokenizer = self.tokenizer_loader.from_pretrained(f"{self.save_path}")
        # Check if GPU is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"[+] Model loaded in {device} complete")
        model = self.model_loader.from_pretrained(f"{self.save_path}").to(device)

        logger.debug("[+] Loading completed")
        return tokenizer, model

    def retrieve(self) -> Tuple:
        """Retriver

        Returns:
            Tuple: tokenizer, model
        """
        return self.tokenizer, self.model
    
    
def create_instance(model_type: str) -> Base:
    try:
        module = importlib.import_module(f"app.engine.instances.{model_type}")
        model_class = getattr(module, f"{model_type}Model")
    except ImportError:
        print(f"Module {model_type} not found.")
    except AttributeError:
        print(f"Class {model_type}Model not found.")
        
    return model_class()
