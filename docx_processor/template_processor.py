#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于docxtpl的Word模板处理器
用于将LLM返回的JSON数据填入Word模板，生成最终的教学设计文档
"""

import os
import json
from typing import Dict, Any, Optional, List
from docxtpl import DocxTemplate
from datetime import datetime

# 导入数据结构定义
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.teaching_design_schema import TeachingDesignData, validate_teaching_design_data

# 导入集中式日志系统
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from utils.logger import get_logger, timing_decorator
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

class TemplateProcessor:
    """Word模板处理器"""
    
    def __init__(self, template_path: str = None):
        """
        初始化模板处理器
        
        Args:
            template_path: 模板文件路径
        """
        if template_path is None:
            # 使用默认模板路径
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            template_path = os.path.join(current_dir, "templates", "teaching_design_template.docx")
        
        self.template_path = template_path
        self.template = None
        self._load_template()
    
    def set_template(self, template_path: str):
        """
        设置模板文件路径
        
        Args:
            template_path: 新的模板文件路径
        """
        self.template_path = template_path
        self._load_template()
    
    def _load_template(self):
        """加载Word模板"""
        try:
            if os.path.exists(self.template_path):
                logger.debug(f"📝 LOADING TEMPLATE: {self.template_path}")
                self.template = DocxTemplate(self.template_path)
                logger.info(f"✅ TEMPLATE LOADED SUCCESSFULLY: {self.template_path}")
            else:
                logger.error(f"❌ TEMPLATE FILE NOT FOUND: {self.template_path}")
                self.template = None
        except Exception as e:
            logger.error(f"❌ TEMPLATE LOADING FAILED: {e}", exc_info=True)
            self.template = None
    
    @timing_decorator("template_processing")
    def process_teaching_design(self, json_data: str, output_path: str) -> Dict[str, Any]:
        """
        处理教学设计数据，生成Word文档
        
        Args:
            json_data: LLM返回的JSON字符串
            output_path: 输出文件路径
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        logger.info(f"📝 STARTING TEMPLATE PROCESSING - Output: {output_path}")
        
        try:
            # 解析JSON数据
            logger.debug("🔍 PARSING JSON DATA")
            data_dict = json.loads(json_data)
            logger.info(f"✅ JSON PARSED SUCCESSFULLY - Keys: {list(data_dict.keys())}")
            
            # 验证数据格式
            logger.debug("✅ VALIDATING DATA FORMAT")
            is_valid, errors = validate_teaching_design_data(data_dict)
            if not is_valid:
                logger.error(f"❌ DATA VALIDATION FAILED - Errors: {errors}")
                return {
                    'success': False,
                    'error': 'invalid_data',
                    'message': '数据格式验证失败',
                    'errors': errors
                }
            logger.info("✅ DATA VALIDATION PASSED")
            
            # 创建教学设计数据对象
            logger.debug("🏗️ CREATING DESIGN DATA OBJECT")
            design_data = TeachingDesignData.from_dict(data_dict)
            logger.info("✅ DESIGN DATA OBJECT CREATED")
            
            # 转换为模板数据格式
            logger.debug("🔄 CONVERTING TO TEMPLATE DATA FORMAT")
            template_data = self._convert_to_template_data(design_data)
            logger.info(f"✅ TEMPLATE DATA CONVERTED - Activities: {len(template_data.get('learning_activities', []))}")
            
            # 生成Word文档
            logger.debug("📄 GENERATING WORD DOCUMENT")
            return self._generate_document(template_data, output_path)
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON PARSING FAILED: {e}", exc_info=True)
            return {
                'success': False,
                'error': 'json_parse_error',
                'message': f'JSON格式错误: {str(e)}'
            }
        except Exception as e:
            logger.error(f"❌ TEMPLATE PROCESSING FAILED: {e}", exc_info=True)
            return {
                'success': False,
                'error': 'processing_error',
                'message': str(e)
            }
    
    def _convert_to_template_data(self, design_data: TeachingDesignData) -> Dict[str, Any]:
        """
        将教学设计数据转换为模板数据格式
        
        Args:
            design_data: 教学设计数据对象
            
        Returns:
            Dict[str, Any]: 模板数据
        """
        # 处理学习目标格式
        learning_objectives = self._format_learning_objectives(design_data.learning_objectives)
        
        # 基本信息
        template_data = {
            'lesson_name': design_data.lesson_name,
            'grade_level': design_data.grade_level,
            'subject': design_data.subject,
            'textbook_version': design_data.textbook_version,
            'lesson_period': design_data.lesson_period,
            'teacher_school': design_data.teacher_school,
            'teacher_name': design_data.teacher_name,
            'summary': design_data.summary,
            'content_analysis': design_data.content_analysis,
            'learner_analysis': design_data.learner_analysis,
            'learning_objectives': learning_objectives,
            'lesson_structure': design_data.lesson_structure,
            'blackboard_design': design_data.blackboard_design,
            'homework_extension': design_data.homework_extension,
            'materials_design': design_data.materials_design,
        }
        
        # 处理学习活动 - 支持表插入形式
        activities = []
        for i, activity in enumerate(design_data.learning_activities):
            activities.append({
                'name': activity.name,
                'teacher_activity': activity.teacher_activity,
                'student_activity': activity.student_activity,
                'activity_intent': activity.activity_intent  # 使用每个活动自己的意图
            })
        
        template_data['learning_activities'] = activities
        
        # 处理思维训练点
        thinking_points = []
        for point in design_data.reflection_thinking_points:
            thinking_points.append({
                'point_type': point.point_type,
                'description': point.description
            })
        
        template_data['reflection_thinking_points'] = thinking_points
        
        return template_data
    
    def _format_learning_objectives(self, learning_objectives: str) -> str:
        """
        格式化学习目标，确保采用序号形式呈现
        
        Args:
            learning_objectives: 学习目标字符串
            
        Returns:
            str: 格式化后的学习目标字符串（序号形式）
        """
        try:
            # 尝试解析JSON格式
            import json
            objectives_data = json.loads(learning_objectives)
            
            if isinstance(objectives_data, list):
                # 如果是列表格式，转换为编号列表
                formatted_objectives = []
                for i, obj in enumerate(objectives_data, 1):
                    if isinstance(obj, dict) and 'objective' in obj:
                        formatted_objectives.append(f"{i}. {obj['objective']}")
                    else:
                        formatted_objectives.append(f"{i}. {str(obj)}")
                return '\n'.join(formatted_objectives)
            else:
                return learning_objectives
                
        except (json.JSONDecodeError, TypeError):
            # 如果不是JSON格式，检查是否已经是序号格式
            lines = learning_objectives.strip().split('\n')
            formatted_lines = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                    
                # 检查是否已经有序号
                if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                    formatted_lines.append(line)
                else:
                    # 如果没有序号，添加序号
                    formatted_lines.append(f"{i+1}. {line}")
            
            return '\n'.join(formatted_lines)
    
    def _generate_document(self, template_data: Dict[str, Any], output_path: str) -> Dict[str, Any]:
        """
        生成Word文档
        
        Args:
            template_data: 模板数据
            output_path: 输出文件路径
            
        Returns:
            Dict[str, Any]: 生成结果
        """
        try:
            if self.template is None:
                return {
                    'success': False,
                    'error': 'template_not_loaded',
                    'message': '模板未加载'
                }
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 渲染模板
            self.template.render(template_data)
            
            # 保存文档
            self.template.save(output_path)
            
            # 检查文件是否成功创建
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"文档生成成功: {output_path}, 大小: {file_size} bytes")
                
                return {
                    'success': True,
                    'output_path': output_path,
                    'file_size': file_size,
                    'generated_time': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'save_failed',
                    'message': '文档保存失败'
                }
                
        except Exception as e:
            logger.error(f"生成文档失败: {e}")
            return {
                'success': False,
                'error': 'generation_failed',
                'message': str(e)
            }
    
    def process_from_file(self, json_file_path: str, output_path: str) -> Dict[str, Any]:
        """
        从JSON文件处理教学设计
        
        Args:
            json_file_path: JSON文件路径
            output_path: 输出文件路径
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_data = f.read()
            
            return self.process_teaching_design(json_data, output_path)
            
        except Exception as e:
            logger.error(f"从文件处理失败: {e}")
            return {
                'success': False,
                'error': 'file_processing_error',
                'message': str(e)
            }
    
    def get_template_info(self) -> Dict[str, Any]:
        """
        获取模板信息
        
        Returns:
            Dict[str, Any]: 模板信息
        """
        if self.template is None:
            return {
                'loaded': False,
                'template_path': self.template_path,
                'message': '模板未加载'
            }
        
        return {
            'loaded': True,
            'template_path': self.template_path,
            'template_exists': os.path.exists(self.template_path),
            'template_size': os.path.getsize(self.template_path) if os.path.exists(self.template_path) else 0
        }

# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建模板处理器
    processor = TemplateProcessor()
    
    # 获取模板信息
    info = processor.get_template_info()
    print(f"模板信息: {info}")
    
    # 测试数据
    test_json = '''
    {
        "lesson_name": "《春》教学设计",
        "grade_level": "初中一年级",
        "subject": "语文",
        "textbook_version": "人教版",
        "lesson_period": "第1课时",
        "teacher_school": "XX学校",
        "teacher_name": "XX教师",
        "summary": "本课通过引导学生感受春天的美好，培养学生的观察能力和语言表达能力。",
        "content_analysis": "《春》是朱自清的一篇散文，通过描绘春天的景象，表达了作者对春天的喜爱之情。",
        "learner_analysis": "初一学生已经具备一定的阅读能力，但对散文的欣赏还需要进一步引导。",
        "learning_objectives": "1. 能够朗读课文，感受春天的美好（重点）\\n2. 能够分析文章的语言特色（难点）\\n3. 能够仿写春天的片段",
        "lesson_structure": "导入→整体感知→重点研读→拓展延伸→总结",
        "learning_activities": [
            {
                "name": "导入环节",
                "teacher_activity": "播放春天相关的音乐，引导学生回忆春天的景象",
                "student_activity": "听音乐，回忆并分享春天的印象",
                "activity_intent": "通过音乐导入激发学生学习兴趣，营造春天的氛围"
            },
            {
                "name": "整体感知",
                "teacher_activity": "指导学生朗读课文，整体把握文章内容",
                "student_activity": "朗读课文，概括文章主要内容",
                "activity_intent": "通过朗读整体感知文章内容，培养学生语感和理解能力"
            }
        ],
        "blackboard_design": "春\\n春草→春花→春风→春雨\\n生机勃勃 充满希望",
        "homework_extension": "1. 背诵课文第1-3段\\n2. 观察身边的春天，写一段描写春天的文字",
        "materials_design": "多媒体课件、春天相关图片、音乐",
        "reflection_thinking_points": [
            {
                "point_type": "认知冲突",
                "description": "通过对比不同季节的特点，引发学生对春天独特之处的思考"
            },
            {
                "point_type": "思维图示",
                "description": "使用思维导图梳理文章结构，帮助学生理解文章脉络"
            },
            {
                "point_type": "变式运用",
                "description": "通过仿写练习，让学生将学到的写作技巧应用到实际写作中"
            }
        ]
    }
    '''
    
    # 处理教学设计
    result = processor.process_teaching_design(test_json, "test_output.docx")
    print(f"处理结果: {result}")
