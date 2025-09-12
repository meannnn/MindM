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
    activity_intent: str
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
            activity_intent=data.get('activity_intent', ''),
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
                    "student_activity": {"type": "string", "description": "学生活动"}
                },
                "required": ["name", "teacher_activity", "student_activity"]
            }
        },
        "activity_intent": {"type": "string", "description": "活动意图说明"},
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
        "lesson_structure", "learning_activities", "activity_intent",
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
            "student_activity": "听音乐，回忆并分享春天的印象"
        },
        {
            "name": "整体感知",
            "teacher_activity": "指导学生朗读课文，整体把握文章内容",
            "student_activity": "朗读课文，概括文章主要内容"
        }
    ],
    "activity_intent": "通过音乐导入激发学生学习兴趣，通过朗读整体感知文章内容",
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

def validate_teaching_design_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    验证教学设计数据是否符合schema
    
    Args:
        data: 要验证的数据
        
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
                    required_activity_fields = ["name", "teacher_activity", "student_activity"]
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
    
    return len(errors) == 0, errors

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
