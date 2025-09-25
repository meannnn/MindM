# 📊 Logging System Guide

## 🎯 Overview

The application now includes a comprehensive centralized logging system with detailed timing and performance monitoring to help identify bottlenecks in the DOCX generation process.

## 🚀 Features

### ✅ **Centralized Logging System**
- **Single logger instance** across all modules
- **Consistent formatting** with colors and emojis
- **Multiple output targets** (console + file)
- **Configurable log levels** (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### ⏱️ **Performance Monitoring**
- **Automatic timing** for all major operations
- **Stage-by-stage tracking** of document processing
- **Performance summaries** with duration breakdowns
- **Bottleneck identification** through detailed timing

### 📋 **Document Processing Tracking**
- **Upload timing** and file validation
- **Text extraction** performance
- **AI processing** stages and duration
- **Template processing** timing
- **Overall pipeline** performance

## 🛠️ Usage

### **Basic Logging**

```python
from utils.logger import get_logger

logger = get_logger(__name__)

# Different log levels
logger.debug("🔍 Detailed debugging information")
logger.info("ℹ️  General information")
logger.warning("⚠️  Warning messages")
logger.error("❌ Error conditions")
logger.critical("💥 Critical errors")
```

### **Performance Timing**

```python
from utils.logger import timing_decorator, DocumentProcessingLogger

# Automatic timing decorator
@timing_decorator("operation_name")
def my_function():
    # Your code here
    pass

# Manual timing
doc_logger = DocumentProcessingLogger("task_123", logger)
doc_logger.log_upload_start("file.docx", 1024)
# ... processing ...
doc_logger.log_upload_complete(True, "Success")
```

### **Document Processing Pipeline**

```python
# Complete document processing with timing
doc_logger = DocumentProcessingLogger(task_id, logger)

# Upload stage
doc_logger.log_upload_start(filename, file_size)
doc_logger.log_upload_complete(success, details)

# Text extraction stage
doc_logger.log_text_extraction_start()
doc_logger.log_text_extraction_complete(success, text_length)

# AI processing stage
doc_logger.log_ai_processing_start(model_name)
doc_logger.log_ai_processing_stage(stage_name, details)
doc_logger.log_ai_processing_complete(success, response_length, model)

# Validation stage
doc_logger.log_validation_start()
doc_logger.log_validation_complete(success, errors)

# Template processing stage
doc_logger.log_template_processing_start(template_path)
doc_logger.log_template_processing_complete(success, output_path)

# Final summary
doc_logger.log_generation_complete(total_duration, success)
```

## ⚙️ Configuration

### **Environment Variables**

```bash
# Logging configuration
LOG_LEVEL=DEBUG              # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=./logs/app.log      # Log file path
```

### **Logger Setup**

```python
from utils.logger import setup_logger

logger = setup_logger(
    name="my_module",
    log_level="DEBUG",
    log_file="./logs/app.log",
    console_output=True,
    enable_colors=True
)
```

## 📊 Performance Analysis

### **Timing Information**

The system now provides detailed timing for each stage:

```
🚀 STARTING FILE UPLOAD PROCESS - Task ID: abc123
📤 UPLOAD START: document.docx (1024 bytes)
⏱️  END: abc123.upload - ✅ SUCCESS - Duration: 0.234s
📄 TEXT EXTRACTION START: Processing document content
⏱️  END: abc123.extraction - ✅ SUCCESS - Duration: 0.156s
🤖 AI PROCESSING START: Using model qwen-long
📋 STAGE: abc123.ai_processing -> file_preparation - Files uploaded
⏱️  END: abc123.ai_processing - ✅ SUCCESS - Duration: 15.234s
📝 TEMPLATE PROCESSING START: template.docx
⏱️  END: abc123.template - ✅ SUCCESS - Duration: 0.445s
🎉 SUCCESS DOCUMENT GENERATION COMPLETE: Total duration 16.069s
```

### **Performance Summary**

```
📊 PERFORMANCE SUMMARY for abc123:
  - abc123.upload: 0.234s
  - abc123.extraction: 0.156s
  - abc123.ai_processing: 15.234s
  - abc123.template: 0.445s
```

## 🔍 Identifying Bottlenecks

### **Common Performance Issues**

1. **AI Processing (Usually 10-30 seconds)**
   - File upload to Aliyun
   - AI model processing time
   - Response generation

2. **Template Processing (Usually < 1 second)**
   - JSON parsing
   - Data validation
   - Word document generation

3. **File Operations (Usually < 1 second)**
   - File upload validation
   - Text extraction
   - File I/O operations

### **Optimization Tips**

Based on timing data:

- **If AI processing > 30s**: Check network connection, file size, or model selection
- **If template processing > 2s**: Check data complexity or template size
- **If file operations > 2s**: Check disk I/O or file size

## 🧪 Testing

### **Run Logging Tests**

```bash
cd pythondocx/pythondocx
python test_logging.py
```

This will test:
- Basic logging functionality
- Timing decorators
- Document processing logger
- Performance monitoring

### **Check Log Files**

```bash
# View real-time logs
tail -f logs/app.log

# Search for specific operations
grep "Task ID:" logs/app.log

# Find performance bottlenecks
grep "Duration:" logs/app.log | sort -k5 -nr
```

## 📈 Log Analysis

### **Performance Metrics**

```bash
# Find slowest operations
grep "Duration:" logs/app.log | awk '{print $NF}' | sort -nr | head -10

# Count successful vs failed operations
grep -c "SUCCESS" logs/app.log
grep -c "FAILED" logs/app.log

# Average processing times
grep "Total duration" logs/app.log | awk '{print $NF}' | awk '{sum+=$1; count++} END {print sum/count}'
```

### **Error Analysis**

```bash
# Find all errors
grep "❌" logs/app.log

# Find AI processing failures
grep "AI PROCESSING FAILED" logs/app.log

# Find validation errors
grep "VALIDATION FAILED" logs/app.log
```

## 🎨 Log Format

### **Console Output (Colored)**
```
14:30:25 | INFO     | ai_doc_assistant | upload:285 | 🚀 STARTING FILE UPLOAD PROCESS - Task ID: abc123
14:30:25 | DEBUG    | ai_doc_assistant | upload:159 | 📤 UPLOAD START: document.docx (1024 bytes)
14:30:25 | INFO     | ai_doc_assistant | upload:164 | ⏱️  END: abc123.upload - ✅ SUCCESS - Duration: 0.234s
```

### **File Output (Detailed)**
```
2024-01-15 14:30:25 | INFO     | ai_doc_assistant | upload:285 | 🚀 STARTING FILE UPLOAD PROCESS - Task ID: abc123
2024-01-15 14:30:25 | DEBUG    | ai_doc_assistant | upload:159 | 📤 UPLOAD START: document.docx (1024 bytes)
2024-01-15 14:30:25 | INFO     | ai_doc_assistant | upload:164 | ⏱️  END: abc123.upload - ✅ SUCCESS - Duration: 0.234s
```

## 🔧 Troubleshooting

### **Common Issues**

1. **Logs not appearing**
   - Check LOG_LEVEL setting
   - Verify log file permissions
   - Ensure logs directory exists

2. **Performance data missing**
   - Check if timing decorators are applied
   - Verify DocumentProcessingLogger usage
   - Look for timing exceptions

3. **Too much/too little detail**
   - Adjust LOG_LEVEL (DEBUG for more, INFO for less)
   - Modify specific logger levels
   - Use filtering in log analysis

### **Debug Mode**

Enable maximum verbosity:
```bash
export LOG_LEVEL=DEBUG
python app.py
```

This will show:
- All timing information
- Detailed API requests/responses
- File operation details
- Validation steps
- Template processing stages

## 📚 Best Practices

1. **Use appropriate log levels**
   - DEBUG: Detailed debugging info
   - INFO: General operational messages
   - WARNING: Warning conditions
   - ERROR: Error conditions
   - CRITICAL: Critical errors

2. **Include context in messages**
   - Task IDs for tracking
   - File names and sizes
   - Operation durations
   - Error details

3. **Monitor performance regularly**
   - Check logs for bottlenecks
   - Track average processing times
   - Monitor error rates
   - Optimize based on data

4. **Use structured logging**
   - Consistent message formats
   - Include relevant metadata
   - Use emojis for visual scanning
   - Provide actionable information

This logging system will help you identify exactly where the DOCX generation is slow and optimize accordingly!
