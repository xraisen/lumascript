import logging
import sys
from typing import Optional

class Logger:
    def __init__(self, name: str, level: Optional[int] = None):
        """Initialize logger with name and optional level"""
        self.logger = logging.getLogger(name)
        
        # Set level if provided, otherwise use INFO
        self.logger.setLevel(level or logging.INFO)
        
        # Create console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message)
    
    def set_level(self, level: int) -> None:
        """Set logging level"""
        self.logger.setLevel(level) 