"""
模板处理器

专门用于处理Word文档模板，包括占位符识别、替换和内容填充。
"""

import os
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

logger = logging.getLogger(__name__)


class TemplateProcessor:
    """模板处理器"""
    
    def __init__(self, template_path: str):
        """
        初始化模板处理器
        
        Args:
            template_path: 模板文件路径
        """
        self.template_path = template_path
        self.document = None
        self.placeholders = {}
        self.placeholder_pattern = r'\{\{([^}]+)\}\}'
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"模板文件不存在: {template_path}")
        
        self._load_template()
    
    def _load_template(self):
        """加载模板文档"""
        try:
            self.document = Document(self.template_path)
            logger.info(f"成功加载模板: {self.template_path}")
        except Exception as e:
            logger.error(f"加载模板失败: {e}")
            raise
    
    def find_placeholders(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        查找模板中的所有占位符
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: 占位符信息
        """
        placeholders = {
            'text_placeholders': [],
            'table_placeholders': [],
            'image_placeholders': [],
            'style_placeholders': []
        }
        
        try:
            # 在段落中查找占位符
            for para_idx, paragraph in enumerate(self.document.paragraphs):
                for run_idx, run in enumerate(paragraph.runs):
                    if run.text:
                        matches = re.finditer(self.placeholder_pattern, run.text)
                        for match in matches:
                            placeholder_info = {
                                'placeholder': match.group(0),
                                'name': match.group(1).strip(),
                                'paragraph_index': para_idx,
                                'run_index': run_idx,
                                'start_pos': match.start(),
                                'end_pos': match.end(),
                                'type': 'text'
                            }
                            placeholders['text_placeholders'].append(placeholder_info)
            
            # 在表格中查找占位符
            for table_idx, table in enumerate(self.document.tables):
                for row_idx, row in enumerate(table.rows):
                    for cell_idx, cell in enumerate(row.cells):
                        for para_idx, paragraph in enumerate(cell.paragraphs):
                            for run_idx, run in enumerate(paragraph.runs):
                                if run.text:
                                    matches = re.finditer(self.placeholder_pattern, run.text)
                                    for match in matches:
                                        placeholder_info = {
                                            'placeholder': match.group(0),
                                            'name': match.group(1).strip(),
                                            'table_index': table_idx,
                                            'row_index': row_idx,
                                            'cell_index': cell_idx,
                                            'paragraph_index': para_idx,
                                            'run_index': run_idx,
                                            'start_pos': match.start(),
                                            'end_pos': match.end(),
                                            'type': 'table'
                                        }
                                        placeholders['table_placeholders'].append(placeholder_info)
            
            # 查找图片占位符
            for para_idx, paragraph in enumerate(self.document.paragraphs):
                if paragraph.text and re.search(self.placeholder_pattern, paragraph.text):
                    matches = re.finditer(self.placeholder_pattern, paragraph.text)
                    for match in matches:
                        placeholder_name = match.group(1).strip()
                        if 'image' in placeholder_name.lower() or 'picture' in placeholder_name.lower():
                            placeholder_info = {
                                'placeholder': match.group(0),
                                'name': placeholder_name,
                                'paragraph_index': para_idx,
                                'type': 'image'
                            }
                            placeholders['image_placeholders'].append(placeholder_info)
            
            self.placeholders = placeholders
            logger.info(f"找到占位符: 文本 {len(placeholders['text_placeholders'])} 个, "
                       f"表格 {len(placeholders['table_placeholders'])} 个, "
                       f"图片 {len(placeholders['image_placeholders'])} 个")
            
            return placeholders
            
        except Exception as e:
            logger.error(f"查找占位符失败: {e}")
            return placeholders
    
    def replace_placeholder(self, placeholder_name: str, replacement_value: Any, 
                          replacement_type: str = 'text') -> bool:
        """
        替换占位符
        
        Args:
            placeholder_name: 占位符名称
            replacement_value: 替换值
            replacement_type: 替换类型 ('text', 'table', 'image')
            
        Returns:
            bool: 是否替换成功
        """
        try:
            if replacement_type == 'text':
                return self._replace_text_placeholder(placeholder_name, replacement_value)
            elif replacement_type == 'table':
                return self._replace_table_placeholder(placeholder_name, replacement_value)
            elif replacement_type == 'image':
                return self._replace_image_placeholder(placeholder_name, replacement_value)
            else:
                logger.error(f"不支持的替换类型: {replacement_type}")
                return False
                
        except Exception as e:
            logger.error(f"替换占位符失败: {e}")
            return False
    
    def _replace_text_placeholder(self, placeholder_name: str, replacement_value: str) -> bool:
        """替换文本占位符"""
        try:
            placeholder_found = False
            
            # 在段落中查找并替换
            for paragraph in self.document.paragraphs:
                for run in paragraph.runs:
                    if run.text:
                        placeholder = f"{{{{{placeholder_name}}}}}"
                        if placeholder in run.text:
                            run.text = run.text.replace(placeholder, str(replacement_value))
                            placeholder_found = True
            
            # 在表格中查找并替换
            for table in self.document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                if run.text:
                                    placeholder = f"{{{{{placeholder_name}}}}}"
                                    if placeholder in run.text:
                                        run.text = run.text.replace(placeholder, str(replacement_value))
                                        placeholder_found = True
            
            if placeholder_found:
                logger.info(f"替换文本占位符: {placeholder_name}")
                return True
            else:
                logger.warning(f"未找到文本占位符: {placeholder_name}")
                return False
                
        except Exception as e:
            logger.error(f"替换文本占位符失败: {e}")
            return False
    
    def _replace_table_placeholder(self, placeholder_name: str, replacement_data: List[List[str]]) -> bool:
        """替换表格占位符"""
        try:
            placeholder_found = False
            
            for table in self.document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                if run.text:
                                    placeholder = f"{{{{{placeholder_name}}}}}"
                                    if placeholder in run.text:
                                        # 清空单元格内容
                                        cell.text = ""
                                        
                                        # 添加表格数据
                                        if replacement_data:
                                            # 创建表格
                                            new_table = cell.add_table(rows=len(replacement_data), cols=len(replacement_data[0]))
                                            
                                            # 填充数据
                                            for i, row_data in enumerate(replacement_data):
                                                if i < len(new_table.rows):
                                                    for j, cell_data in enumerate(row_data):
                                                        if j < len(new_table.rows[i].cells):
                                                            new_table.rows[i].cells[j].text = str(cell_data)
                                        
                                        placeholder_found = True
            
            if placeholder_found:
                logger.info(f"替换表格占位符: {placeholder_name}")
                return True
            else:
                logger.warning(f"未找到表格占位符: {placeholder_name}")
                return False
                
        except Exception as e:
            logger.error(f"替换表格占位符失败: {e}")
            return False
    
    def _replace_image_placeholder(self, placeholder_name: str, image_path: str) -> bool:
        """替换图片占位符"""
        try:
            placeholder_found = False
            
            if not os.path.exists(image_path):
                logger.error(f"图片文件不存在: {image_path}")
                return False
            
            for paragraph in self.document.paragraphs:
                if paragraph.text:
                    placeholder = f"{{{{{placeholder_name}}}}}"
                    if placeholder in paragraph.text:
                        # 清空段落内容
                        paragraph.clear()
                        
                        # 添加图片
                        paragraph.add_picture(image_path, width=Inches(4))
                        
                        placeholder_found = True
            
            if placeholder_found:
                logger.info(f"替换图片占位符: {placeholder_name}")
                return True
            else:
                logger.warning(f"未找到图片占位符: {placeholder_name}")
                return False
                
        except Exception as e:
            logger.error(f"替换图片占位符失败: {e}")
            return False
    
    def fill_template(self, data: Dict[str, Any]) -> bool:
        """
        填充模板数据
        
        Args:
            data: 填充数据
            
        Returns:
            bool: 是否填充成功
        """
        try:
            success_count = 0
            total_count = 0
            
            for key, value in data.items():
                total_count += 1
                
                # 确定替换类型
                replacement_type = 'text'
                if isinstance(value, list) and value and isinstance(value[0], list):
                    replacement_type = 'table'
                elif isinstance(value, str) and (value.endswith('.jpg') or value.endswith('.png') or 
                                               value.endswith('.gif') or value.endswith('.bmp')):
                    replacement_type = 'image'
                
                # 执行替换
                if self.replace_placeholder(key, value, replacement_type):
                    success_count += 1
            
            logger.info(f"模板填充完成: {success_count}/{total_count} 个占位符替换成功")
            return success_count == total_count
            
        except Exception as e:
            logger.error(f"填充模板失败: {e}")
            return False
    
    def add_content_after_placeholder(self, placeholder_name: str, content: List[Dict[str, Any]]) -> bool:
        """
        在占位符后添加内容
        
        Args:
            placeholder_name: 占位符名称
            content: 要添加的内容
            
        Returns:
            bool: 是否添加成功
        """
        try:
            placeholder_found = False
            
            # 查找占位符位置
            for para_idx, paragraph in enumerate(self.document.paragraphs):
                if paragraph.text:
                    placeholder = f"{{{{{placeholder_name}}}}}"
                    if placeholder in paragraph.text:
                        # 替换占位符
                        paragraph.text = paragraph.text.replace(placeholder, "")
                        
                        # 在段落后添加内容
                        self._add_content_after_paragraph(para_idx, content)
                        placeholder_found = True
                        break
            
            if placeholder_found:
                logger.info(f"在占位符后添加内容: {placeholder_name}")
                return True
            else:
                logger.warning(f"未找到占位符: {placeholder_name}")
                return False
                
        except Exception as e:
            logger.error(f"在占位符后添加内容失败: {e}")
            return False
    
    def _add_content_after_paragraph(self, paragraph_index: int, content: List[Dict[str, Any]]):
        """在指定段落后添加内容"""
        try:
            # 获取段落对象
            paragraph = self.document.paragraphs[paragraph_index]
            
            # 在段落后添加内容
            for item in content:
                item_type = item.get('type', 'paragraph')
                
                if item_type == 'heading':
                    new_para = self.document.add_heading(item.get('text', ''), item.get('level', 1))
                elif item_type == 'paragraph':
                    new_para = self.document.add_paragraph(item.get('text', ''))
                elif item_type == 'list':
                    for list_item in item.get('items', []):
                        self.document.add_paragraph(list_item, style='List Bullet')
                elif item_type == 'table':
                    if item.get('data'):
                        self.document.add_table(
                            rows=len(item['data']),
                            cols=len(item['data'][0]) if item['data'] else 0
                        )
                elif item_type == 'page_break':
                    self.document.add_page_break()
                
                # 设置样式
                if 'style' in item and hasattr(new_para, 'style'):
                    new_para.style = item['style']
            
        except Exception as e:
            logger.error(f"在段落后添加内容失败: {e}")
    
    def validate_template(self) -> Dict[str, Any]:
        """
        验证模板
        
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            validation_result = {
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'placeholder_count': 0,
                'missing_placeholders': []
            }
            
            # 查找所有占位符
            placeholders = self.find_placeholders()
            all_placeholders = []
            
            for placeholder_list in placeholders.values():
                all_placeholders.extend(placeholder_list)
            
            validation_result['placeholder_count'] = len(all_placeholders)
            
            # 检查占位符格式
            for placeholder_info in all_placeholders:
                placeholder_name = placeholder_info['name']
                
                # 检查占位符名称是否为空
                if not placeholder_name.strip():
                    validation_result['errors'].append(f"空占位符名称: {placeholder_info['placeholder']}")
                    validation_result['is_valid'] = False
                
                # 检查占位符名称是否包含特殊字符
                if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', placeholder_name):
                    validation_result['warnings'].append(f"占位符名称可能不规范: {placeholder_name}")
            
            # 检查重复占位符
            placeholder_names = [p['name'] for p in all_placeholders]
            duplicate_names = set([name for name in placeholder_names if placeholder_names.count(name) > 1])
            
            if duplicate_names:
                validation_result['warnings'].append(f"发现重复占位符: {list(duplicate_names)}")
            
            logger.info(f"模板验证完成: {'通过' if validation_result['is_valid'] else '失败'}")
            return validation_result
            
        except Exception as e:
            logger.error(f"验证模板失败: {e}")
            return {'is_valid': False, 'errors': [str(e)], 'warnings': [], 'placeholder_count': 0}
    
    def get_template_info(self) -> Dict[str, Any]:
        """
        获取模板信息
        
        Returns:
            Dict[str, Any]: 模板信息
        """
        try:
            placeholders = self.find_placeholders()
            
            info = {
                'template_path': self.template_path,
                'template_size': os.path.getsize(self.template_path),
                'paragraph_count': len(self.document.paragraphs),
                'table_count': len(self.document.tables),
                'placeholder_count': sum(len(pl) for pl in placeholders.values()),
                'placeholder_types': {
                    'text': len(placeholders['text_placeholders']),
                    'table': len(placeholders['table_placeholders']),
                    'image': len(placeholders['image_placeholders'])
                },
                'placeholders': placeholders
            }
            
            return info
            
        except Exception as e:
            logger.error(f"获取模板信息失败: {e}")
            return {}
    
    def save_filled_template(self, output_path: str) -> bool:
        """
        保存填充后的模板
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            bool: 是否保存成功
        """
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            self.document.save(output_path)
            logger.info(f"填充后的模板已保存: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存填充后的模板失败: {e}")
            return False


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建模板处理器
    processor = TemplateProcessor("template.docx")
    
    # 查找占位符
    placeholders = processor.find_placeholders()
    print(f"找到占位符: {placeholders}")
    
    # 验证模板
    validation = processor.validate_template()
    print(f"模板验证结果: {validation}")
    
    # 填充模板数据
    data = {
        'title': '教学设计文档',
        'author': '张老师',
        'school': 'XX学校',
        'course_name': '数学',
        'grade': '三年级',
        'date': '2024-01-15'
    }
    
    success = processor.fill_template(data)
    print(f"模板填充: {'成功' if success else '失败'}")
    
    # 保存填充后的模板
    processor.save_filled_template("filled_template.docx")
    
    # 获取模板信息
    info = processor.get_template_info()
    print(f"模板信息: {info}")