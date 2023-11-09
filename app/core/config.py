import os
from enum import Enum
from typing import List, Union, Optional
from pydantic import BaseSettings, AnyHttpUrl, validator, SecretStr
from multiprocessing import cpu_count


class AppConfig(BaseSettings.Config):
    """
    Config for settings classes that allows for
    combining Setings classes with different env_prefix settings.

    Taken from here:
    https://github.com/pydantic/pydantic/issues/1727#issuecomment-658881926
    """

    case_sensitive = True

    @classmethod
    def prepare_field(cls, field) -> None:
        if "env_names" in field.field_info.extra:
            return
        return super().prepare_field(field)


class AppEnvironment(str, Enum):
    """
    Enum for app environments.
    """

    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Application settings.
    """
    class Config(AppConfig):
        env_prefix = ""

    APP_NAME: str = "Generic HF app"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    API_KEY: SecretStr
    LOG_LEVEL: str = "DEBUG"
    CDN_BASE_URL: str
    
    DEFAULT_MODEL_PATH: str = "./hf_models/models"
    
    MODEL_TYPE: str = "SUM"
    MODEL_TASK: str = "summarization"
    MODEL_NAME: str = "facebook/bart-large-cnn"
    # NER_MODEL_NAME: str = "xlm-roberta-large-finetuned-conll03-english"
    # KEY_MODEL_NAME: str = "ml6team/keyphrase-extraction-kbir-inspec"
    
    @property
    def VERBOSE(self) -> bool:
        """
        Used for setting verbose flag in LlamaIndex modules.
        """
        return self.LOG_LEVEL == "DEBUG"

    @validator("LOG_LEVEL", pre=True)
    def assemble_log_level(cls, v: str) -> str:
        """Preprocesses the log level to ensure its validity."""
        v = v.strip().upper()
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid log level: " + str(v))
        return v

    @property
    def ENVIRONMENT(self) -> AppEnvironment:
        """Returns the app environment."""
        return AppEnvironment.LOCAL

    @property
    def UVICORN_WORKER_COUNT(self) -> int:
        if self.ENVIRONMENT == AppEnvironment.LOCAL:
            return int(cpu_count*2 + 1)
        return 3

    class Config(AppConfig):
        env_prefix = ""


settings = Settings()
# os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY