"""
Word文档生成器

基于python-docx库实现Word文档的创建和生成功能。
参考：https://python-docx.readthedocs.io/en/latest/

功能包括：
- 创建新文档
- 添加标题和段落
- 设置文本格式
- 插入表格和图片
- 应用样式
"""

import os
import logging
from typing import Dict, List, Any, Optional, Union
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_UNDERLINE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.shared import OxmlElement, qn

logger = logging.getLogger(__name__)


class DocumentGenerator:
    """Word文档生成器"""
    
    def __init__(self, template_path: Optional[str] = None):
        """
        初始化文档生成器
        
        Args:
            template_path: 模板文件路径（可选）
        """
        self.template_path = template_path
        self.document = None
        self._initialize_document()
    
    def _initialize_document(self):
        """初始化文档"""
        try:
            if self.template_path and os.path.exists(self.template_path):
                self.document = Document(self.template_path)
                logger.info(f"使用模板创建文档: {self.template_path}")
            else:
                self.document = Document()
                logger.info("创建新文档")
        except Exception as e:
            logger.error(f"初始化文档失败: {e}")
            self.document = Document()
    
    def add_heading(self, text: str, level: int = 1, style: Optional[str] = None) -> Any:
        """
        添加标题
        
        Args:
            text: 标题文本
            level: 标题级别 (0-9)
            style: 自定义样式名称
            
        Returns:
            段落对象
        """
        try:
            if style:
                heading = self.document.add_heading(text, level)
                heading.style = style
            else:
                heading = self.document.add_heading(text, level)
            
            logger.info(f"添加标题: {text} (级别: {level})")
            return heading
            
        except Exception as e:
            logger.error(f"添加标题失败: {e}")
            return None
    
    def add_paragraph(self, text: str = "", style: Optional[str] = None) -> Any:
        """
        添加段落
        
        Args:
            text: 段落文本
            style: 段落样式
            
        Returns:
            段落对象
        """
        try:
            paragraph = self.document.add_paragraph(text)
            
            if style:
                paragraph.style = style
            
            logger.info(f"添加段落: {text[:50]}...")
            return paragraph
            
        except Exception as e:
            logger.error(f"添加段落失败: {e}")
            return None
    
    def add_formatted_paragraph(self, text: str, **formatting) -> Any:
        """
        添加格式化段落
        
        Args:
            text: 段落文本
            **formatting: 格式参数
            
        Returns:
            段落对象
        """
        try:
            paragraph = self.document.add_paragraph()
            run = paragraph.add_run(text)
            
            # 应用格式
            self._apply_run_formatting(run, **formatting)
            
            logger.info(f"添加格式化段落: {text[:50]}...")
            return paragraph
            
        except Exception as e:
            logger.error(f"添加格式化段落失败: {e}")
            return None
    
    def add_table(self, data: List[List[str]], headers: Optional[List[str]] = None, 
                  style: Optional[str] = None) -> Any:
        """
        添加表格
        
        Args:
            data: 表格数据
            headers: 表头（可选）
            style: 表格样式
            
        Returns:
            表格对象
        """
        try:
            # 计算表格尺寸
            rows = len(data)
            if headers:
                rows += 1
            cols = len(data[0]) if data else 0
            
            if cols == 0:
                logger.warning("表格数据为空")
                return None
            
            # 创建表格
            table = self.document.add_table(rows=rows, cols=cols)
            
            # 设置表格样式
            if style:
                table.style = style
            
            # 添加表头
            if headers:
                header_row = table.rows[0]
                for i, header in enumerate(headers):
                    if i < len(header_row.cells):
                        header_row.cells[i].text = header
                        # 设置表头格式
                        self._format_header_cell(header_row.cells[i])
            
            # 添加数据行
            start_row = 1 if headers else 0
            for i, row_data in enumerate(data):
                if start_row + i < len(table.rows):
                    row = table.rows[start_row + i]
                    for j, cell_data in enumerate(row_data):
                        if j < len(row.cells):
                            row.cells[j].text = str(cell_data)
            
            logger.info(f"添加表格: {rows}行 x {cols}列")
            return table
            
        except Exception as e:
            logger.error(f"添加表格失败: {e}")
            return None
    
    def add_list(self, items: List[str], ordered: bool = False, style: Optional[str] = None) -> List[Any]:
        """
        添加列表
        
        Args:
            items: 列表项
            ordered: 是否为有序列表
            style: 列表样式
            
        Returns:
            段落对象列表
        """
        try:
            paragraphs = []
            
            for item in items:
                if ordered:
                    paragraph = self.document.add_paragraph(item, style='List Number')
                else:
                    paragraph = self.document.add_paragraph(item, style='List Bullet')
                
                if style:
                    paragraph.style = style
                
                paragraphs.append(paragraph)
            
            logger.info(f"添加列表: {len(items)} 项")
            return paragraphs
            
        except Exception as e:
            logger.error(f"添加列表失败: {e}")
            return []
    
    def add_image(self, image_path: str, width: Optional[float] = None, 
                  height: Optional[float] = None, caption: Optional[str] = None) -> Any:
        """
        添加图片
        
        Args:
            image_path: 图片文件路径
            width: 图片宽度（英寸）
            height: 图片高度（英寸）
            caption: 图片说明
            
        Returns:
            段落对象
        """
        try:
            if not os.path.exists(image_path):
                logger.error(f"图片文件不存在: {image_path}")
                return None
            
            # 添加图片
            if width and height:
                paragraph = self.document.add_picture(image_path, width=Inches(width), height=Inches(height))
            elif width:
                paragraph = self.document.add_picture(image_path, width=Inches(width))
            elif height:
                paragraph = self.document.add_picture(image_path, height=Inches(height))
            else:
                paragraph = self.document.add_picture(image_path, width=Inches(4))
            
            # 添加图片说明
            if caption:
                caption_para = self.document.add_paragraph(caption)
                caption_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                caption_para.style = 'Caption'
            
            logger.info(f"添加图片: {image_path}")
            return paragraph
            
        except Exception as e:
            logger.error(f"添加图片失败: {e}")
            return None
    
    def add_page_break(self):
        """添加分页符"""
        try:
            self.document.add_page_break()
            logger.info("添加分页符")
        except Exception as e:
            logger.error(f"添加分页符失败: {e}")
    
    def add_hyperlink(self, text: str, url: str) -> Any:
        """
        添加超链接
        
        Args:
            text: 链接文本
            url: 链接地址
            
        Returns:
            段落对象
        """
        try:
            paragraph = self.document.add_paragraph()
            run = paragraph.add_run(text)
            
            # 创建超链接
            hyperlink = self._create_hyperlink(url, text)
            paragraph._element.append(hyperlink)
            
            logger.info(f"添加超链接: {text} -> {url}")
            return paragraph
            
        except Exception as e:
            logger.error(f"添加超链接失败: {e}")
            return None
    
    def _create_hyperlink(self, url: str, text: str) -> Any:
        """创建超链接元素"""
        try:
            hyperlink = OxmlElement('w:hyperlink')
            hyperlink.set(qn('r:id'), url)
            
            run = OxmlElement('w:r')
            run_properties = OxmlElement('w:rPr')
            
            # 设置超链接样式
            color = OxmlElement('w:color')
            color.set(qn('w:val'), '0563C1')
            run_properties.append(color)
            
            underline = OxmlElement('w:u')
            underline.set(qn('w:val'), 'single')
            run_properties.append(underline)
            
            run.append(run_properties)
            
            text_element = OxmlElement('w:t')
            text_element.text = text
            run.append(text_element)
            
            hyperlink.append(run)
            return hyperlink
            
        except Exception as e:
            logger.error(f"创建超链接元素失败: {e}")
            return None
    
    def _apply_run_formatting(self, run: Any, **formatting):
        """应用文本运行格式"""
        try:
            if 'bold' in formatting:
                run.bold = formatting['bold']
            
            if 'italic' in formatting:
                run.italic = formatting['italic']
            
            if 'underline' in formatting:
                run.underline = formatting['underline']
            
            if 'font_name' in formatting:
                run.font.name = formatting['font_name']
            
            if 'font_size' in formatting:
                run.font.size = Pt(formatting['font_size'])
            
            if 'font_color' in formatting:
                if isinstance(formatting['font_color'], str):
                    # 假设是十六进制颜色
                    color = formatting['font_color'].lstrip('#')
                    rgb = RGBColor(int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))
                    run.font.color.rgb = rgb
                else:
                    run.font.color.rgb = formatting['font_color']
            
        except Exception as e:
            logger.error(f"应用文本格式失败: {e}")
    
    def _format_header_cell(self, cell: Any):
        """格式化表头单元格"""
        try:
            # 设置表头为粗体
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True
            
            # 设置单元格垂直居中对齐
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            
        except Exception as e:
            logger.error(f"格式化表头单元格失败: {e}")
    
    def create_style(self, name: str, style_type: str = 'paragraph', **properties) -> bool:
        """
        创建自定义样式
        
        Args:
            name: 样式名称
            style_type: 样式类型 ('paragraph', 'character', 'table')
            **properties: 样式属性
            
        Returns:
            bool: 是否创建成功
        """
        try:
            # 确定样式类型
            if style_type == 'paragraph':
                style_type_enum = WD_STYLE_TYPE.PARAGRAPH
            elif style_type == 'character':
                style_type_enum = WD_STYLE_TYPE.CHARACTER
            elif style_type == 'table':
                style_type_enum = WD_STYLE_TYPE.TABLE
            else:
                logger.error(f"不支持的样式类型: {style_type}")
                return False
            
            # 创建样式
            style = self.document.styles.add_style(name, style_type_enum)
            
            # 应用属性
            if 'font_name' in properties:
                style.font.name = properties['font_name']
            
            if 'font_size' in properties:
                style.font.size = Pt(properties['font_size'])
            
            if 'bold' in properties:
                style.font.bold = properties['bold']
            
            if 'italic' in properties:
                style.font.italic = properties['italic']
            
            if 'alignment' in properties:
                alignment_map = {
                    'left': WD_PARAGRAPH_ALIGNMENT.LEFT,
                    'center': WD_PARAGRAPH_ALIGNMENT.CENTER,
                    'right': WD_PARAGRAPH_ALIGNMENT.RIGHT,
                    'justify': WD_PARAGRAPH_ALIGNMENT.JUSTIFY
                }
                if properties['alignment'] in alignment_map:
                    style.paragraph_format.alignment = alignment_map[properties['alignment']]
            
            logger.info(f"创建样式: {name}")
            return True
            
        except Exception as e:
            logger.error(f"创建样式失败: {e}")
            return False
    
    def set_document_properties(self, **properties):
        """
        设置文档属性
        
        Args:
            **properties: 文档属性
        """
        try:
            core_props = self.document.core_properties
            
            if 'title' in properties:
                core_props.title = properties['title']
            
            if 'author' in properties:
                core_props.author = properties['author']
            
            if 'subject' in properties:
                core_props.subject = properties['subject']
            
            if 'keywords' in properties:
                core_props.keywords = properties['keywords']
            
            if 'comments' in properties:
                core_props.comments = properties['comments']
            
            logger.info("设置文档属性")
            
        except Exception as e:
            logger.error(f"设置文档属性失败: {e}")
    
    def save_document(self, output_path: str) -> bool:
        """
        保存文档
        
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
            logger.info(f"文档已保存: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存文档失败: {e}")
            return False
    
    def generate_from_template(self, template_data: Dict[str, Any], output_path: str) -> bool:
        """
        基于模板数据生成文档
        
        Args:
            template_data: 模板数据
            output_path: 输出文件路径
            
        Returns:
            bool: 是否生成成功
        """
        try:
            # 设置文档属性
            if 'properties' in template_data:
                self.set_document_properties(**template_data['properties'])
            
            # 添加内容
            if 'content' in template_data:
                self._add_content_from_data(template_data['content'])
            
            # 保存文档
            return self.save_document(output_path)
            
        except Exception as e:
            logger.error(f"基于模板生成文档失败: {e}")
            return False
    
    def _add_content_from_data(self, content_data: List[Dict[str, Any]]):
        """根据数据添加内容"""
        try:
            for item in content_data:
                item_type = item.get('type', 'paragraph')
                
                if item_type == 'heading':
                    self.add_heading(
                        item.get('text', ''),
                        item.get('level', 1),
                        item.get('style')
                    )
                
                elif item_type == 'paragraph':
                    if 'formatting' in item:
                        self.add_formatted_paragraph(
                            item.get('text', ''),
                            **item['formatting']
                        )
                    else:
                        self.add_paragraph(
                            item.get('text', ''),
                            item.get('style')
                        )
                
                elif item_type == 'table':
                    self.add_table(
                        item.get('data', []),
                        item.get('headers'),
                        item.get('style')
                    )
                
                elif item_type == 'list':
                    self.add_list(
                        item.get('items', []),
                        item.get('ordered', False),
                        item.get('style')
                    )
                
                elif item_type == 'image':
                    self.add_image(
                        item.get('path', ''),
                        item.get('width'),
                        item.get('height'),
                        item.get('caption')
                    )
                
                elif item_type == 'page_break':
                    self.add_page_break()
                
                elif item_type == 'hyperlink':
                    self.add_hyperlink(
                        item.get('text', ''),
                        item.get('url', '')
                    )
            
            logger.info("根据数据添加内容完成")
            
        except Exception as e:
            logger.error(f"根据数据添加内容失败: {e}")
    
    def get_document_info(self) -> Dict[str, Any]:
        """
        获取文档信息
        
        Returns:
            Dict[str, Any]: 文档信息
        """
        try:
            info = {
                'paragraph_count': len(self.document.paragraphs),
                'table_count': len(self.document.tables),
                'section_count': len(self.document.sections),
                'style_count': len(self.document.styles),
                'properties': {
                    'title': self.document.core_properties.title,
                    'author': self.document.core_properties.author,
                    'subject': self.document.core_properties.subject,
                    'keywords': self.document.core_properties.keywords
                }
            }
            
            return info
            
        except Exception as e:
            logger.error(f"获取文档信息失败: {e}")
            return {}


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建文档生成器
    generator = DocumentGenerator()
    
    # 设置文档属性
    generator.set_document_properties(
        title="示例文档",
        author="AI Assistant",
        subject="python-docx示例",
        keywords="python, docx, 文档生成"
    )
    
    # 添加标题
    generator.add_heading("文档标题", 0)
    generator.add_heading("第一章", 1)
    generator.add_heading("1.1 小节", 2)
    
    # 添加段落
    generator.add_paragraph("这是一个普通段落。")
    generator.add_formatted_paragraph(
        "这是一个格式化段落，包含粗体和斜体文本。",
        bold=True,
        italic=True,
        font_size=14,
        font_color="#FF0000"
    )
    
    # 添加表格
    table_data = [
        ["姓名", "年龄", "职业"],
        ["张三", "25", "工程师"],
        ["李四", "30", "设计师"],
        ["王五", "28", "产品经理"]
    ]
    generator.add_table(table_data, style="Table Grid")
    
    # 添加列表
    generator.add_list(["项目一", "项目二", "项目三"], ordered=True)
    
    # 添加分页符
    generator.add_page_break()
    
    # 添加超链接
    generator.add_hyperlink("访问官网", "https://www.example.com")
    
    # 保存文档
    generator.save_document("example_generated.docx")
    
    # 获取文档信息
    info = generator.get_document_info()
    print(f"文档信息: {info}")