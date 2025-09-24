#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教学设计JSON Schema定义
用于约束LLM输出的JSON格式，确保数据能正确填入Word模板
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json

@dataclass
class ActivityInfo:
    """学习活动信息"""
    name: str  # 活动名称
    teacher_activity: str  # 教师活动
    student_activity: str  # 学生活动
    activity_intent: str  # 活动意图

@dataclass
class ThinkingPoint:
    """思维训练点"""
    point_type: str  # 类型：认知冲突、思维图示、变式运用
    description: str  # 说明

@dataclass
class TeachingDesignData:
    """教学设计数据结构"""
    # 基本信息
    lesson_name: str
    grade_level: str
    subject: str
    textbook_version: str
    lesson_period: str
    teacher_school: str
    teacher_name: str
    
    # 教学设计内容
    summary: str
    content_analysis: str
    learner_analysis: str
    learning_objectives: str
    lesson_structure: str
    learning_activities: List[ActivityInfo]
    blackboard_design: str
    homework_extension: str
    materials_design: str
    reflection_thinking_points: List[ThinkingPoint]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return asdict(self)
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TeachingDesignData':
        """从字典创建对象"""
        # 处理学习活动列表
        activities = []
        if 'learning_activities' in data:
            for activity_data in data['learning_activities']:
                activities.append(ActivityInfo(**activity_data))
        
        # 处理思维训练点列表
        thinking_points = []
        if 'reflection_thinking_points' in data:
            for point_data in data['reflection_thinking_points']:
                thinking_points.append(ThinkingPoint(**point_data))
        
        # 创建对象
        return cls(
            lesson_name=data.get('lesson_name', ''),
            grade_level=data.get('grade_level', ''),
            subject=data.get('subject', ''),
            textbook_version=data.get('textbook_version', ''),
            lesson_period=data.get('lesson_period', ''),
            teacher_school=data.get('teacher_school', ''),
            teacher_name=data.get('teacher_name', ''),
            summary=data.get('summary', ''),
            content_analysis=data.get('content_analysis', ''),
            learner_analysis=data.get('learner_analysis', ''),
            learning_objectives=data.get('learning_objectives', ''),
            lesson_structure=data.get('lesson_structure', ''),
            learning_activities=activities,
            blackboard_design=data.get('blackboard_design', ''),
            homework_extension=data.get('homework_extension', ''),
            materials_design=data.get('materials_design', ''),
            reflection_thinking_points=thinking_points
        )

# JSON Schema定义（用于验证LLM输出）
TEACHING_DESIGN_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "lesson_name": {"type": "string", "description": "课例名称"},
        "grade_level": {"type": "string", "description": "学段年级"},
        "subject": {"type": "string", "description": "学科"},
        "textbook_version": {"type": "string", "description": "教材版本"},
        "lesson_period": {"type": "string", "description": "课时说明"},
        "teacher_school": {"type": "string", "description": "教师单位"},
        "teacher_name": {"type": "string", "description": "教师姓名"},
        "summary": {"type": "string", "description": "摘要"},
        "content_analysis": {"type": "string", "description": "教学内容分析"},
        "learner_analysis": {"type": "string", "description": "学习者分析"},
        "learning_objectives": {"type": "string", "description": "学习目标及重难点"},
        "lesson_structure": {"type": "string", "description": "课例结构"},
        "learning_activities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "活动名称"},
                    "teacher_activity": {"type": "string", "description": "教师活动"},
                    "student_activity": {"type": "string", "description": "学生活动"},
                    "activity_intent": {"type": "string", "description": "活动意图"}
                },
                "required": ["name", "teacher_activity", "student_activity", "activity_intent"]
            }
        },
        "blackboard_design": {"type": "string", "description": "板书设计"},
        "homework_extension": {"type": "string", "description": "作业与拓展学习设计"},
        "materials_design": {"type": "string", "description": "素材设计"},
        "reflection_thinking_points": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "point_type": {"type": "string", "description": "思维训练点类型"},
                    "description": {"type": "string", "description": "说明"}
                },
                "required": ["point_type", "description"]
            }
        }
    },
    "required": [
        "lesson_name", "grade_level", "subject", "textbook_version", 
        "lesson_period", "teacher_school", "teacher_name", "summary",
        "content_analysis", "learner_analysis", "learning_objectives",
        "lesson_structure", "learning_activities",
        "blackboard_design", "homework_extension", "materials_design",
        "reflection_thinking_points"
    ]
}

# 示例数据
EXAMPLE_TEACHING_DESIGN = {
    "lesson_name": "《春》教学设计",
    "grade_level": "初中一年级",
    "subject": "语文",
    "textbook_version": "人教版",
    "lesson_period": "第1课时",
    "teacher_school": "XX学校",
    "teacher_name": "XX教师",
    "summary": "本课通过引导学生感受春天的美好，培养学生的观察能力和语言表达能力...",
    "content_analysis": "《春》是朱自清的一篇散文，通过描绘春天的景象，表达了作者对春天的喜爱之情...",
    "learner_analysis": "初一学生已经具备一定的阅读能力，但对散文的欣赏还需要进一步引导...",
    "learning_objectives": "1. 能够朗读课文，感受春天的美好（重点）\n2. 能够分析文章的语言特色（难点）\n3. 能够仿写春天的片段",
    "lesson_structure": "导入→整体感知→重点研读→拓展延伸→总结",
    "learning_activities": [
        {
            "name": "导入环节",
            "teacher_activity": "播放春天相关的音乐，引导学生回忆春天的景象",
            "student_activity": "听音乐，回忆并分享春天的印象",
            "activity_intent": "通过音乐导入激发学生学习兴趣，营造春天的氛围"
        },
        {
            "name": "整体感知环节",
            "teacher_activity": "指导学生朗读课文，整体把握文章内容",
            "student_activity": "朗读课文，概括文章主要内容",
            "activity_intent": "通过朗读整体感知文章内容，培养学生语感和理解能力"
        },
        {
            "name": "重点研读环节",
            "teacher_activity": "引导学生分析文章的重点段落和关键语句",
            "student_activity": "小组合作，分析重点段落，体会语言特色",
            "activity_intent": "深入理解文章重点内容，提高学生的分析能力和语言鉴赏能力"
        },
        {
            "name": "拓展延伸环节",
            "teacher_activity": "组织学生进行仿写练习，联系生活实际",
            "student_activity": "仿写春天片段，分享自己的春天体验",
            "activity_intent": "将所学知识运用到实际写作中，培养学生的表达能力"
        },
        {
            "name": "总结环节",
            "teacher_activity": "引导学生总结本课学习内容，布置作业",
            "student_activity": "总结学习收获，明确课后任务",
            "activity_intent": "巩固学习成果，为后续学习做准备"
        }
    ],
    "blackboard_design": "春\n春草→春花→春风→春雨\n生机勃勃 充满希望",
    "homework_extension": "1. 背诵课文第1-3段\n2. 观察身边的春天，写一段描写春天的文字",
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

def validate_teaching_design_data(data: Dict[str, Any], original_content: str = None) -> tuple[bool, List[str]]:
    """
    验证教学设计数据是否符合schema
    
    Args:
        data: 要验证的数据
        original_content: 原始文档内容，用于验证内容覆盖完整性
        
    Returns:
        tuple: (是否有效, 错误信息列表)
    """
    errors = []
    
    # 检查必需字段
    required_fields = TEACHING_DESIGN_JSON_SCHEMA["required"]
    for field in required_fields:
        if field not in data:
            errors.append(f"缺少必需字段: {field}")
    
    # 检查学习活动列表
    if "learning_activities" in data:
        if not isinstance(data["learning_activities"], list):
            errors.append("learning_activities 必须是列表")
        else:
            for i, activity in enumerate(data["learning_activities"]):
                if not isinstance(activity, dict):
                    errors.append(f"学习活动 {i+1} 必须是字典")
                else:
                    required_activity_fields = ["name", "teacher_activity", "student_activity", "activity_intent"]
                    for field in required_activity_fields:
                        if field not in activity:
                            errors.append(f"学习活动 {i+1} 缺少字段: {field}")
    
    # 检查思维训练点列表
    if "reflection_thinking_points" in data:
        if not isinstance(data["reflection_thinking_points"], list):
            errors.append("reflection_thinking_points 必须是列表")
        else:
            for i, point in enumerate(data["reflection_thinking_points"]):
                if not isinstance(point, dict):
                    errors.append(f"思维训练点 {i+1} 必须是字典")
                else:
                    required_point_fields = ["point_type", "description"]
                    for field in required_point_fields:
                        if field not in point:
                            errors.append(f"思维训练点 {i+1} 缺少字段: {field}")
    
    # 验证lesson_structure与learning_activities的一致性
    if "lesson_structure" in data and "learning_activities" in data:
        lesson_structure = data["lesson_structure"]
        learning_activities = data["learning_activities"]
        
        if isinstance(lesson_structure, str) and isinstance(learning_activities, list):
            # 解析lesson_structure中的环节
            # 常见的分隔符：→、->、-、→、→
            structure_parts = []
            for separator in ["→", "->", "-", "→", "→"]:
                if separator in lesson_structure:
                    structure_parts = [part.strip() for part in lesson_structure.split(separator)]
                    break
            
            # 如果没有找到分隔符，尝试其他方式解析
            if not structure_parts:
                # 尝试按常见教学环节关键词分割
                keywords = ["导入", "新知", "探究", "巩固", "练习", "总结", "拓展", "延伸"]
                structure_parts = []
                current_part = ""
                for char in lesson_structure:
                    current_part += char
                    for keyword in keywords:
                        if keyword in current_part and current_part.strip():
                            structure_parts.append(current_part.strip())
                            current_part = ""
                            break
                if current_part.strip():
                    structure_parts.append(current_part.strip())
            
            # 检查learning_activities数量是否与structure_parts匹配
            if len(structure_parts) > 0:
                # 限制最多8个环节
                if len(structure_parts) > 8:
                    errors.append(f"课例结构环节数量({len(structure_parts)})超过最大限制(8个)，请简化教学环节")
                elif len(learning_activities) > 8:
                    errors.append(f"学习活动数量({len(learning_activities)})超过最大限制(8个)，请减少学习活动")
                elif len(learning_activities) < len(structure_parts):
                    errors.append(f"学习活动数量({len(learning_activities)})少于课例结构环节数量({len(structure_parts)})，请确保每个结构环节都有对应的学习活动")
                elif len(learning_activities) > len(structure_parts) + 2:  # 允许有2个额外的活动作为容错
                    errors.append(f"学习活动数量({len(learning_activities)})明显多于课例结构环节数量({len(structure_parts)})，请检查是否有多余的活动")
    
    # 内容覆盖检查（如果有原始文档内容）
    if original_content and "learning_activities" in data:
        content_coverage_errors = _check_content_coverage(data, original_content)
        errors.extend(content_coverage_errors)
    
    return len(errors) == 0, errors

def _check_content_coverage(data: Dict[str, Any], original_content: str) -> List[str]:
    """
    检查教学设计是否完整覆盖了原始文档内容
    
    Args:
        data: 教学设计数据
        original_content: 原始文档内容
        
    Returns:
        List[str]: 内容覆盖相关的错误信息
    """
    errors = []
    
    # 提取学习活动中的内容关键词
    learning_activities = data.get("learning_activities", [])
    activity_content_keywords = []
    
    for activity in learning_activities:
        if isinstance(activity, dict):
            # 从活动名称、教师活动、学生活动和活动意图中提取关键词
            activity_text = " ".join([
                activity.get("name", ""),
                activity.get("teacher_activity", ""),
                activity.get("student_activity", ""),
                activity.get("activity_intent", "")
            ])
            activity_content_keywords.append(activity_text.lower())
    
    # 分析原始文档内容，提取重要概念和知识点
    original_lower = original_content.lower()
    
    # 检查是否有明显的内容遗漏
    # 这里可以添加更复杂的自然语言处理逻辑
    # 目前使用简单的关键词匹配
    
    # 检查学习目标是否基于文档内容
    learning_objectives = data.get("learning_objectives", "")
    if learning_objectives:
        objectives_lower = learning_objectives.lower()
        # 如果学习目标过于通用，可能没有基于文档内容
        generic_terms = ["了解", "知道", "掌握", "理解", "学会"]
        if all(term in objectives_lower for term in generic_terms[:3]):
            errors.append("学习目标可能过于通用，请确保基于上传文档的具体内容制定目标")
    
    # 检查课例结构是否包含足够的环节
    lesson_structure = data.get("lesson_structure", "")
    if lesson_structure:
        # 检查是否有基本的教学环节
        required_phases = ["导入", "总结"]
        structure_lower = lesson_structure.lower()
        missing_phases = [phase for phase in required_phases if phase not in structure_lower]
        if missing_phases:
            errors.append(f"课例结构缺少基本环节: {', '.join(missing_phases)}")
    
    # 检查学习活动的多样性
    if len(learning_activities) < 3:
        errors.append("学习活动数量可能不足以覆盖文档中的所有重要内容，建议增加教学环节")
    
    # 检查是否有重复的活动意图
    activity_intents = [activity.get("activity_intent", "") for activity in learning_activities if isinstance(activity, dict)]
    if len(activity_intents) != len(set(activity_intents)):
        errors.append("发现重复的活动意图，请确保每个学习活动都有独特的目的")
    
    # 检查内容相符性
    content_alignment_errors = _check_content_alignment(data, original_content)
    errors.extend(content_alignment_errors)
    
    return errors

def _check_content_alignment(data: Dict[str, Any], original_content: str) -> List[str]:
    """
    检查教学设计是否与文档内容相符
    
    Args:
        data: 教学设计数据
        original_content: 原始文档内容
        
    Returns:
        List[str]: 内容相符性相关的错误信息
    """
    errors = []
    
    original_lower = original_content.lower()
    
    # 检查是否包含了文档中提到的教学方法
    teaching_methods_in_doc = _extract_teaching_methods(original_content)
    if teaching_methods_in_doc:
        learning_activities = data.get("learning_activities", [])
        activity_texts = []
        for activity in learning_activities:
            if isinstance(activity, dict):
                activity_text = " ".join([
                    activity.get("name", ""),
                    activity.get("teacher_activity", ""),
                    activity.get("student_activity", ""),
                    activity.get("activity_intent", "")
                ]).lower()
                activity_texts.append(activity_text)
        
        # 检查是否体现了文档中的主要教学方法（至少体现一半）
        methods_found = 0
        for method in teaching_methods_in_doc:
            method_found = any(method.lower() in text for text in activity_texts)
            if method_found:
                methods_found += 1
        
        if methods_found < len(teaching_methods_in_doc) // 2:  # 至少体现一半的方法
            errors.append(f"文档中提到了多种教学方法，但教学设计中体现不足，建议增加小组讨论、合作探究等活动")
    
    # 检查是否包含了文档中的教学要求（放宽检查条件）
    teaching_requirements = _extract_teaching_requirements(original_content)
    if teaching_requirements:
        learning_objectives = data.get("learning_objectives", "").lower()
        lesson_structure = data.get("lesson_structure", "").lower()
        
        # 检查核心关键词是否体现
        core_keywords = ["掌握", "理解", "运用", "分析", "重点", "难点"]
        found_keywords = []
        for keyword in core_keywords:
            if keyword in learning_objectives or keyword in lesson_structure:
                found_keywords.append(keyword)
        
        if len(found_keywords) < 2:  # 至少要有2个核心关键词
            errors.append("教学设计中缺少文档要求的核心教学要素，请确保包含掌握、理解、运用等关键要求")
    
    # 检查知识点分离情况
    knowledge_points = _extract_knowledge_points(original_content)
    if len(knowledge_points) > 1:
        learning_activities = data.get("learning_activities", [])
        if len(learning_activities) < len(knowledge_points):
            errors.append(f"文档中包含{len(knowledge_points)}个不同知识点，但教学设计只有{len(learning_activities)}个环节，建议为每个知识点设计独立的环节")
    
    return errors

def _extract_teaching_methods(content: str) -> List[str]:
    """
    从文档中提取教学方法
    
    Args:
        content: 文档内容
        
    Returns:
        List[str]: 教学方法列表
    """
    methods = []
    
    # 常见的教学方法关键词
    method_keywords = [
        "讨论", "探究", "合作学习", "小组活动", "实验", "观察", "分析", "比较",
        "归纳", "演绎", "案例教学", "情境教学", "问题导向", "任务驱动",
        "自主学习", "合作探究", "实践操作", "演示", "讲解", "练习"
    ]
    
    content_lower = content.lower()
    for keyword in method_keywords:
        if keyword in content_lower:
            methods.append(keyword)
    
    return methods

def _extract_teaching_requirements(content: str) -> List[str]:
    """
    从文档中提取教学要求
    
    Args:
        content: 文档内容
        
    Returns:
        List[str]: 教学要求列表
    """
    requirements = []
    
    # 常见的教学要求关键词
    requirement_keywords = [
        "掌握", "理解", "运用", "分析", "评价", "创造", "应用", "学会",
        "能够", "可以", "必须", "需要", "要求", "目标", "重点", "难点"
    ]
    
    content_lower = content.lower()
    sentences = content.split('。')
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for keyword in requirement_keywords:
            if keyword in sentence_lower and len(sentence.strip()) > 5:
                requirements.append(sentence.strip())
                break
    
    return requirements[:5]  # 限制返回前5个要求

def _extract_knowledge_points(content: str) -> List[str]:
    """
    从文档中提取知识点
    
    Args:
        content: 文档内容
        
    Returns:
        List[str]: 知识点列表
    """
    knowledge_points = []
    
    # 常见的知识点指示词
    knowledge_indicators = [
        "概念", "定义", "原理", "定理", "公式", "方法", "技巧", "技能",
        "性质", "特征", "特点", "规律", "法则", "规则", "步骤", "过程",
        "类型", "分类", "结构", "组成", "关系", "联系", "区别", "对比"
    ]
    
    sentences = content.split('。')
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for indicator in knowledge_indicators:
            if indicator in sentence_lower and len(sentence.strip()) > 5:
                knowledge_points.append(sentence.strip())
                break
    
    return list(set(knowledge_points))  # 去重

# 使用示例
if __name__ == "__main__":
    # 创建示例数据
    design_data = TeachingDesignData.from_dict(EXAMPLE_TEACHING_DESIGN)
    
    # 验证数据
    is_valid, errors = validate_teaching_design_data(design_data.to_dict())
    
    if is_valid:
        print("数据验证通过")
        print("JSON格式:")
        print(design_data.to_json())
    else:
        print("数据验证失败:")
        for error in errors:
            print(f"- {error}")
