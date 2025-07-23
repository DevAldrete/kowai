"""
Structured logging configuration for KowAI Backend
"""
import logging
import json
from datetime import datetime
from contextvars import ContextVar
from typing import Dict, Any, Optional


# Context variables for correlation tracking
correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)
user_id: ContextVar[Optional[str]] = ContextVar('user_id', default=None)


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id.get(),
            "user_id": user_id.get()
        }
        
        # Add execution time if available
        if hasattr(record, 'execution_time'):
            log_entry["execution_time"] = record.execution_time
        
        # Add request information if available
        if hasattr(record, 'request_method'):
            log_entry["request_method"] = record.request_method
        
        if hasattr(record, 'request_path'):
            log_entry["request_path"] = record.request_path
        
        if hasattr(record, 'response_status'):
            log_entry["response_status"] = record.response_status
        
        # Add persona information if available
        if hasattr(record, 'persona_id'):
            log_entry["persona_id"] = record.persona_id
        
        if hasattr(record, 'persona_type'):
            log_entry["persona_type"] = record.persona_type
        
        # Add AI processing information
        if hasattr(record, 'ai_model'):
            log_entry["ai_model"] = record.ai_model
        
        if hasattr(record, 'ai_tokens_used'):
            log_entry["ai_tokens_used"] = record.ai_tokens_used
        
        # Add workflow information
        if hasattr(record, 'workflow_id'):
            log_entry["workflow_id"] = record.workflow_id
        
        if hasattr(record, 'task_id'):
            log_entry["task_id"] = record.task_id
        
        # Add exception information
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
        
        return json.dumps(log_entry, default=str)


def setup_logging() -> logging.Logger:
    """Setup application logging configuration"""
    # Create formatter
    formatter = StructuredFormatter()
    
    # Create handler
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    # Setup root logger
    logger = logging.getLogger("kowai")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Disable other loggers to avoid noise
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("uvicorn.error").disabled = True
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name"""
    return logging.getLogger(f"kowai.{name}")


def set_correlation_id(corr_id: str) -> None:
    """Set correlation ID for request tracking"""
    correlation_id.set(corr_id)


def set_user_id(uid: str) -> None:
    """Set user ID for request tracking"""
    user_id.set(uid)


def get_correlation_id() -> Optional[str]:
    """Get current correlation ID"""
    return correlation_id.get()


def get_user_id() -> Optional[str]:
    """Get current user ID"""
    return user_id.get()