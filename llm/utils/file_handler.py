"""
简化的文件处理器

处理Word文件上传和基本文本提取。
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

# 导入集中式日志系统
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from utils.logger import get_logger, timing_decorator
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


class FileHandler:
    """简化的文件处理器"""
    
    def __init__(self, upload_dir: str = "./uploads", max_file_size: int = 10 * 1024 * 1024):
        """
        初始化文件处理器
        
        Args:
            upload_dir: 上传文件存储目录
            max_file_size: 最大文件大小（字节）
        """
        self.upload_dir = upload_dir
        self.max_file_size = max_file_size
        self.allowed_extensions = {'.docx', '.doc'}
        
        # 确保上传目录存在
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
        
        logger.info(f"✅ FILE HANDLER INITIALIZED - Upload directory: {self.upload_dir}")
    
    def validate_file(self, file_path: str, filename: str) -> Dict[str, Any]:
        """
        验证上传的文件
        
        Args:
            file_path: 文件路径
            filename: 文件名
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }
        
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                validation_result['is_valid'] = False
                validation_result['errors'].append("文件不存在")
                return validation_result
            
            # 检查文件大小
            file_size = os.path.getsize(file_path)
            validation_result['file_info']['size'] = file_size
            
            if file_size > self.max_file_size:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"文件大小超过限制 ({self.max_file_size / 1024 / 1024:.1f}MB)")
            
            # 检查文件扩展名
            _, ext = os.path.splitext(filename.lower())
            validation_result['file_info']['extension'] = ext
            
            if ext not in self.allowed_extensions:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"不支持的文件格式: {ext}")
            
            # 检查文件是否为空
            if file_size == 0:
                validation_result['is_valid'] = False
                validation_result['errors'].append("文件为空")
            
            # 添加文件信息
            validation_result['file_info'].update({
                'filename': filename,
                'path': file_path,
                'upload_time': datetime.now().isoformat()
            })
            
            logger.info(f"✅ FILE VALIDATION COMPLETE: {filename} - {'PASSED' if validation_result['is_valid'] else 'FAILED'}")
            return validation_result
            
        except Exception as e:
            logger.error(f"❌ FILE VALIDATION FAILED: {e}", exc_info=True)
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"验证过程出错: {str(e)}")
            return validation_result
    
    def save_uploaded_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        保存上传的文件
        
        Args:
            file_content: 文件内容
            filename: 文件名
            
        Returns:
            Dict[str, Any]: 保存结果
        """
        try:
            # 生成唯一文件名
            file_id = str(uuid.uuid4())
            _, ext = os.path.splitext(filename)
            unique_filename = f"{file_id}{ext}"
            file_path = os.path.join(self.upload_dir, unique_filename)
            
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # 验证保存的文件
            validation = self.validate_file(file_path, filename)
            
            if validation['is_valid']:
                result = {
                    'success': True,
                    'file_id': file_id,
                    'original_filename': filename,
                    'saved_filename': unique_filename,
                    'file_path': file_path,
                    'file_size': len(file_content),
                    'upload_time': datetime.now().isoformat()
                }
                logger.info(f"文件保存成功: {filename} -> {unique_filename}")
                return result
            else:
                # 删除无效文件
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                return {
                    'success': False,
                    'error': 'validation_failed',
                    'message': '文件验证失败',
                    'validation_errors': validation['errors']
                }
                
        except Exception as e:
            logger.error(f"文件保存失败: {e}")
            return {
                'success': False,
                'error': 'save_failed',
                'message': str(e)
            }
    
    def extract_text_from_docx(self, file_path: str) -> Dict[str, Any]:
        """
        从Word文档中提取文本内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 提取结果
        """
        try:
            # 简单的文本提取，不依赖复杂的docx模块
            import zipfile
            import xml.etree.ElementTree as ET
            
            # Word文档实际上是一个zip文件
            with zipfile.ZipFile(file_path, 'r') as docx:
                # 读取主文档内容
                document = docx.read('word/document.xml')
                root = ET.fromstring(document)
                
                # 提取所有文本
                text_content = []
                for elem in root.iter():
                    if elem.text:
                        text_content.append(elem.text)
                
                extracted_text = '\n'.join(text_content)
                
                # 清理文本
                extracted_text = extracted_text.strip()
                
                result = {
                    'success': True,
                    'text_content': extracted_text,
                    'file_path': file_path,
                    'extract_time': datetime.now().isoformat()
                }
                
                logger.info(f"文本提取成功: {file_path}")
                return result
                
        except Exception as e:
            logger.error(f"文本提取失败: {e}")
            return {
                'success': False,
                'error': 'extraction_failed',
                'message': str(e)
            }
    
    def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文件信息
        
        Args:
            file_id: 文件ID
            
        Returns:
            Optional[Dict[str, Any]]: 文件信息
        """
        try:
            # 查找文件
            for filename in os.listdir(self.upload_dir):
                if filename.startswith(file_id):
                    file_path = os.path.join(self.upload_dir, filename)
                    if os.path.exists(file_path):
                        stat = os.stat(file_path)
                        return {
                            'file_id': file_id,
                            'filename': filename,
                            'file_path': file_path,
                            'file_size': stat.st_size,
                            'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat()
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"获取文件信息失败: {e}")
            return None
    
    def delete_file(self, file_id: str) -> bool:
        """
        删除文件
        
        Args:
            file_id: 文件ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 查找并删除文件
            for filename in os.listdir(self.upload_dir):
                if filename.startswith(file_id):
                    file_path = os.path.join(self.upload_dir, filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logger.info(f"文件删除成功: {filename}")
                        return True
            
            logger.warning(f"文件未找到: {file_id}")
            return False
            
        except Exception as e:
            logger.error(f"文件删除失败: {e}")
            return False

    def get_template_file_content(self, template_path: str = None) -> Dict[str, Any]:
        """
        获取模板文件内容
        
        Args:
            template_path: 模板文件路径，如果为None则使用默认路径
            
        Returns:
            Dict[str, Any]: 模板文件内容
        """
        try:
            # 如果没有指定模板路径，使用默认路径
            if template_path is None:
                # 查找项目根目录下的模板文件
                current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                template_path = os.path.join(current_dir, "2023【教学设计模板】思维发展型课堂-XX学校-XX教师.docx")
            
            # 检查模板文件是否存在
            if not os.path.exists(template_path):
                return {
                    'success': False,
                    'error': 'template_not_found',
                    'message': f'模板文件不存在: {template_path}'
                }
            
            # 提取模板文件文本内容
            text_result = self.extract_text_from_docx(template_path)
            
            if text_result['success']:
                return {
                    'success': True,
                    'template_path': template_path,
                    'template_content': text_result['text_content'],
                    'extract_time': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'template_extraction_failed',
                    'message': text_result.get('message', '模板文件内容提取失败')
                }
                
        except Exception as e:
            logger.error(f"获取模板文件内容失败: {e}")
            return {
                'success': False,
                'error': 'template_error',
                'message': str(e)
            }


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建文件处理器
    file_handler = FileHandler()
    
    # 测试文件保存
    test_content = b"test content"
    result = file_handler.save_uploaded_file(test_content, "test.docx")
    print(f"文件保存结果: {result}")
    
    if result['success']:
        # 测试文本提取
        extract_result = file_handler.extract_text_from_docx(result['file_path'])
        print(f"文本提取结果: {extract_result}")
        
        # 清理测试文件
        file_handler.delete_file(result['file_id'])