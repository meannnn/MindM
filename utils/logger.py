#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralized logging system with timing and performance monitoring
"""

import os
import sys
import time
import logging
import functools
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from pathlib import Path

class PerformanceLogger:
    """Performance monitoring and timing logger"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.timers: Dict[str, float] = {}
        self.stages: Dict[str, Dict[str, Any]] = {}
    
    def start_timer(self, operation_id: str, description: str = ""):
        """Start timing an operation"""
        self.timers[operation_id] = time.time()
        self.stages[operation_id] = {
            'description': description,
            'start_time': datetime.now().isoformat(),
            'start_timestamp': time.time()
        }
        self.logger.info(f"⏱️  START: {operation_id} - {description}")
    
    def end_timer(self, operation_id: str, success: bool = True, details: str = ""):
        """End timing an operation and log the duration"""
        if operation_id not in self.timers:
            self.logger.warning(f"Timer {operation_id} was not started")
            return
        
        duration = time.time() - self.timers[operation_id]
        status = "✅ SUCCESS" if success else "❌ FAILED"
        
        self.stages[operation_id].update({
            'end_time': datetime.now().isoformat(),
            'duration': duration,
            'success': success,
            'details': details
        })
        
        self.logger.info(f"⏱️  END: {operation_id} - {status} - Duration: {duration:.3f}s {details}")
        
        # Remove from active timers
        del self.timers[operation_id]
        
        return duration
    
    def log_stage(self, operation_id: str, stage_name: str, details: str = ""):
        """Log a stage within an operation"""
        if operation_id not in self.stages:
            self.logger.warning(f"Operation {operation_id} not found for stage logging")
            return
        
        stage_key = f"{operation_id}.{stage_name}"
        self.stages[stage_key] = {
            'operation_id': operation_id,
            'stage_name': stage_name,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        
        self.logger.info(f"📋 STAGE: {operation_id} -> {stage_name} - {details}")
    
    def get_performance_summary(self, operation_id: str) -> Dict[str, Any]:
        """Get performance summary for an operation"""
        summary = {}
        
        # Find all stages for this operation
        for key, stage_data in self.stages.items():
            if key.startswith(operation_id):
                summary[key] = stage_data
        
        return summary

def timing_decorator(operation_name: str, logger: Optional[logging.Logger] = None):
    """Decorator to automatically time function execution"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if logger is None:
                log = logging.getLogger(func.__module__)
            else:
                log = logger
            
            perf_logger = PerformanceLogger(log)
            
            # Start timing
            perf_logger.start_timer(operation_name, f"Executing {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                perf_logger.end_timer(operation_name, success=True)
                return result
            except Exception as e:
                perf_logger.end_timer(operation_name, success=False, details=f"Error: {str(e)}")
                raise
        
        return wrapper
    return decorator

class ColoredFormatter(logging.Formatter):
    """Colored log formatter for better readability"""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_logger(
    name: str = "ai_doc_assistant",
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True,
    enable_colors: bool = True
) -> logging.Logger:
    """
    Setup centralized logger with proper formatting and handlers
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        console_output: Whether to output to console
        enable_colors: Whether to enable colored console output
    
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Set level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        if enable_colors:
            console_handler.setFormatter(ColoredFormatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                datefmt='%H:%M:%S'
            ))
        else:
            console_handler.setFormatter(simple_formatter)
        
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Always log everything to file
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """
    Get logger instance. If name is None, uses the caller's module name.
    
    Args:
        name: Logger name (optional)
    
    Returns:
        Logger instance
    """
    if name is None:
        # Get caller's module name
        frame = sys._getframe(1)
        name = frame.f_globals.get('__name__', 'ai_doc_assistant')
    
    return logging.getLogger(name)

class DocumentProcessingLogger:
    """Specialized logger for document processing operations"""
    
    def __init__(self, operation_id: str, logger: Optional[logging.Logger] = None):
        self.operation_id = operation_id
        self.logger = logger or get_logger()
        self.performance = PerformanceLogger(self.logger)
        self.stages = []
    
    def log_upload_start(self, filename: str, file_size: int):
        """Log file upload start"""
        self.performance.start_timer(f"{self.operation_id}.upload", f"Uploading {filename}")
        self.logger.info(f"📤 UPLOAD START: {filename} ({file_size} bytes)")
    
    def log_upload_complete(self, success: bool, details: str = ""):
        """Log file upload completion"""
        self.performance.end_timer(f"{self.operation_id}.upload", success, details)
        status = "✅ SUCCESS" if success else "❌ FAILED"
        self.logger.info(f"📤 UPLOAD COMPLETE: {status} - {details}")
    
    def log_text_extraction_start(self):
        """Log text extraction start"""
        self.performance.start_timer(f"{self.operation_id}.extraction", "Extracting text from document")
        self.logger.info(f"📄 TEXT EXTRACTION START: Processing document content")
    
    def log_text_extraction_complete(self, success: bool, text_length: int = 0):
        """Log text extraction completion"""
        self.performance.end_timer(f"{self.operation_id}.extraction", success)
        status = "✅ SUCCESS" if success else "❌ FAILED"
        self.logger.info(f"📄 TEXT EXTRACTION COMPLETE: {status} - Extracted {text_length} characters")
    
    def log_ai_processing_start(self, model: str = "unknown"):
        """Log AI processing start"""
        self.performance.start_timer(f"{self.operation_id}.ai_processing", f"AI processing with {model}")
        self.logger.info(f"🤖 AI PROCESSING START: Using model {model}")
    
    def log_ai_processing_stage(self, stage: str, details: str = ""):
        """Log AI processing stage"""
        self.performance.log_stage(f"{self.operation_id}.ai_processing", stage, details)
    
    def log_ai_processing_complete(self, success: bool, response_length: int = 0, model: str = ""):
        """Log AI processing completion"""
        self.performance.end_timer(f"{self.operation_id}.ai_processing", success)
        status = "✅ SUCCESS" if success else "❌ FAILED"
        self.logger.info(f"🤖 AI PROCESSING COMPLETE: {status} - Generated {response_length} characters using {model}")
    
    def log_validation_start(self):
        """Log data validation start"""
        self.performance.start_timer(f"{self.operation_id}.validation", "Validating AI response data")
        self.logger.info(f"✅ VALIDATION START: Checking data format and content")
    
    def log_validation_complete(self, success: bool, errors: list = None):
        """Log data validation completion"""
        self.performance.end_timer(f"{self.operation_id}.validation", success)
        status = "✅ SUCCESS" if success else "❌ FAILED"
        error_count = len(errors) if errors else 0
        self.logger.info(f"✅ VALIDATION COMPLETE: {status} - {error_count} errors found")
        if errors:
            for error in errors:
                self.logger.warning(f"⚠️  VALIDATION ERROR: {error}")
    
    def log_template_processing_start(self, template_path: str):
        """Log template processing start"""
        self.performance.start_timer(f"{self.operation_id}.template", f"Processing template {template_path}")
        self.logger.info(f"📝 TEMPLATE PROCESSING START: {template_path}")
    
    def log_template_processing_complete(self, success: bool, output_path: str = ""):
        """Log template processing completion"""
        self.performance.end_timer(f"{self.operation_id}.template", success)
        status = "✅ SUCCESS" if success else "❌ FAILED"
        self.logger.info(f"📝 TEMPLATE PROCESSING COMPLETE: {status} - Output: {output_path}")
    
    def log_generation_complete(self, total_duration: float, success: bool):
        """Log overall generation completion"""
        status = "🎉 SUCCESS" if success else "💥 FAILED"
        self.logger.info(f"{status} DOCUMENT GENERATION COMPLETE: Total duration {total_duration:.3f}s")
        
        # Log performance summary
        self.logger.info(f"📊 PERFORMANCE SUMMARY for {self.operation_id}:")
        summary = self.performance.get_performance_summary(self.operation_id)
        for stage_id, stage_data in summary.items():
            if 'duration' in stage_data:
                self.logger.info(f"  - {stage_id}: {stage_data['duration']:.3f}s")

# Initialize default logger
default_logger = setup_logger(
    name="ai_doc_assistant",
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_file=os.getenv("LOG_FILE", "./logs/app.log"),
    console_output=True,
    enable_colors=True
)

# Export commonly used items
__all__ = [
    'setup_logger',
    'get_logger',
    'PerformanceLogger',
    'DocumentProcessingLogger',
    'timing_decorator',
    'default_logger'
]


