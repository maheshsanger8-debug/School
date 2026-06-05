"""
Logging configuration for the AI Agent system.

Provides structured logging with file and console output.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from app.config import settings


def setup_logging():
    """Configure logging for the application."""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler - rotating daily
    file_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "agent.log",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "agent_error.log",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module."""
    return logging.getLogger(name)
