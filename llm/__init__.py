"""
简化的LLM模块

基于阿里云百炼API实现的大语言模型集成模块，提供简单的对话功能。

主要功能：
- 阿里云百炼API客户端
- 基本文件处理
- 简单的聊天功能

作者：AI Assistant
版本：1.0.0
"""

from .clients.aliyun_client import AliyunClient
from .utils.file_handler import FileHandler

__version__ = "1.0.0"
__author__ = "AI Assistant"

__all__ = [
    'AliyunClient',
    'FileHandler'
]