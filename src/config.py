"""Configuration management for GEO Expert Agent"""

import logging
import sys
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    openai_api_key: str
    perplexity_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./geo_agent.db"
    
    # Vector Store
    chroma_db_path: str = "./chroma_db"
    
    # LLM Settings
    default_model: str = "gpt-4-turbo-preview"
    embedding_model: str = "text-embedding-3-small"
    max_tokens: int = 4000
    temperature: float = 0.7
    
    # Agent Settings
    max_iterations: int = 10
    max_concurrent_requests: int = 5
    
    # Logging Settings
    log_level: str = "INFO"
    log_format: str = "%(levelname)s | %(name)s | %(message)s"
    log_file: Optional[str] = None  # Set to None to disable file logging
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def setup_logging():
    """Configure logging for the application"""
    # Create formatters
    formatter = logging.Formatter(settings.log_format)
    
    # Console handler with immediate flush
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level))
    console_handler.setFormatter(formatter)
    
    # File handler (if specified)
    handlers = [console_handler]
    if settings.log_file:
        file_handler = logging.FileHandler(settings.log_file)
        file_handler.setLevel(logging.DEBUG)  # File gets all logs
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
        print(f"💾 Logging to file: {settings.log_file}", flush=True)
    else:
        print("📺 Logging to console only (file logging disabled)", flush=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
        force=True  # Force reconfiguration
    )
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)  # Suppress telemetry errors
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    # Force flush on all log messages
    sys.stdout.flush()
    sys.stderr.flush()


# Initialize logging
setup_logging()


