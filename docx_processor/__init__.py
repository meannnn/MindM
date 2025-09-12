"""
Word文档处理模块

基于python-docx库实现Word文档的解析、生成和模板处理功能。

主要功能：
- 文档解析：提取文本、表格、图片、格式信息
- 文档生成：创建新的Word文档
- 模板处理：基于模板填充内容
- 格式保持：保持原有文档的格式和样式

作者：AI Assistant
版本：1.0.0
"""

from .parsers.document_parser import DocumentParser
from .generators.document_generator import DocumentGenerator
from .template_processor import TemplateProcessor
from .utils.document_utils import DocumentUtils

__version__ = "1.0.0"
__author__ = "AI Assistant"

__all__ = [
    'DocumentParser',
    'DocumentGenerator', 
    'TemplateProcessor',
    'DocumentUtils'
]