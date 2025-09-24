#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教学设计生成提示词
用于指导LLM生成符合JSON格式的教学设计数据
"""

def get_teaching_design_prompt(user_file_content: str, template_file_content: str) -> str:
    """
    获取教学设计生成提示词
    
    Args:
        user_file_content: 用户上传文件的文本内容
        template_file_content: 模板文件的文本内容
        
    Returns:
        str: 完整的提示词
    """
    
    prompt = f"""你是一位精通教学法和课程设计的专家。请基于"思维发展型课堂"模型，根据用户提供的学习材料，创建一份全面、高质量的教学设计。

**重要：请严格按照以下JSON格式输出结果，不要包含任何其他文字或解释。**

**输入材料：**
1. 用户上传的学习材料内容：
{user_file_content}

2. 教学设计模板内容：
{template_file_content}

**输出要求：**
请分析学习材料，并严格按照以下JSON格式输出教学设计数据：

```json
{{
    "lesson_name": "课例名称（使用学习材料的标题或核心主题）",
    "grade_level": "学段年级（如：小学一年级、初中二年级、高中一年级）",
    "subject": "学科（如：语文、数学、英语、物理、化学、生物、历史、地理、政治）",
    "textbook_version": "教材版本（如：人教版、苏教版、北师大版等，或填写'根据所给材料'）",
    "lesson_period": "第1课时",
    "teacher_school": "XX学校",
    "teacher_name": "XX教师",
    "summary": "摘要（300-500字，概括课程核心主题、传统教学痛点、本课教学方法特色）",
    "content_analysis": "教学内容分析（分析核心知识点和技能要求，在课程体系中的位置）",
    "learner_analysis": "学习者分析（根据学段年级描述学生特征、已有知识水平、认知发展阶段）",
    "learning_objectives": "学习目标及重难点（3-4个具体可测量的目标，使用行为动词，标注重点和难点）",
    "lesson_structure": "课例结构（整体教学流程，如：导入→新知探究→巩固练习→总结与拓展）",
    "learning_activities": [
        {{
            "name": "活动环节名称",
            "teacher_activity": "教师活动描述",
            "student_activity": "学生活动描述",
            "activity_intent": "该活动的教学意图和目的"
        }},
        {{
            "name": "活动环节名称",
            "teacher_activity": "教师活动描述",
            "student_activity": "学生活动描述",
            "activity_intent": "该活动的教学意图和目的"
        }}
    ],
    "blackboard_design": "板书设计（用文本描述板书布局，包括关键术语、图示和总结）",
    "homework_extension": "作业与拓展学习设计（1-2个家庭作业或拓展活动）",
    "materials_design": "素材设计（学习单、练习纸等，如无则写'本课未设计额外学习素材'）",
    "reflection_thinking_points": [
        {{
            "point_type": "认知冲突",
            "description": "找出1-2个学生可能遇到挑战性或反直觉观点的地方（100字以内）"
        }},
        {{
            "point_type": "思维图示",
            "description": "找出1-2个使用思维工具（思维导图、流程图、对比图）的实例（100字以内）"
        }},
        {{
            "point_type": "变式运用",
            "description": "找出1-2个通过变化练习或案例深化学生理解的例子（100字以内）"
        }}
    ]
}}
```

**内容分析指导：**
在开始设计lesson_structure之前，请先仔细分析上传文档：
1. 识别文档中的所有知识点、概念、原理、方法或技能
2. 确定每个知识点的复杂程度和教学要求
3. 分析知识点之间的关系和逻辑顺序
4. 确定哪些知识点需要独立的教学环节
5. 规划整体教学流程，确保每个知识点都得到充分教授
6. 识别文档中已有的教学活动建议或教学要求
7. 分析文档中的教学方法、活动设计、评价方式等教学要素

**内容相符与优化原则：**
- 如果文档中已经包含教学活动建议，教学设计应该在此基础上进行优化和完善
- 如果文档中提到了具体的教学方法，应该在设计中体现并改进这些方法
- 如果文档中明确了教学要求，教学设计必须完全满足这些要求
- 在满足文档要求的基础上，可以运用思维发展型课堂的理念进行优化
- 优化应该体现在：更好的思维训练、更清晰的活动意图、更有效的学习方式

**内容生成指南：**

**重要：lesson_structure与learning_activities的对应关系**
- lesson_structure描述了整体教学流程（如：导入→新知探究→巩固练习→总结与拓展）
- learning_activities必须为lesson_structure中的每个环节设计对应的学习活动
- 例如：如果lesson_structure是"导入→新知探究→巩固练习→总结与拓展"，那么learning_activities必须包含4个活动，分别对应导入环节、新知探究环节、巩固练习环节、总结与拓展环节
- 每个learning_activity的name字段应该明确标识对应的教学环节

**关键要求：lesson_structure必须完整覆盖教学内容**
- lesson_structure的设计必须确保覆盖上传文档中的所有知识点和教学内容
- 每个教学环节都应该对应文档中的具体知识内容或技能要求
- 不能遗漏文档中提到的任何重要概念、原理、方法或技能
- 如果文档包含多个知识点，lesson_structure应该设计相应的环节来逐一处理
- 确保从导入到总结的整个流程能够完整地教授文档要求的所有知识内容

**知识点分离原则：**
- 不同的知识点必须在不同的教学环节中教授，不能混在一起
- 每个环节应该专注于一个核心知识点或技能
- 如果文档涉及多个概念，需要为每个概念设计独立的环节
- 复杂的概念可以分解为多个子环节，但每个子环节仍应保持焦点明确

1. **课例名称**：使用学习材料的标题或核心主题
2. **学段年级**：根据材料内容复杂程度推断合适的学段年级
3. **学科**：识别对应的学科
4. **摘要**：300-500字，包含核心主题、传统教学痛点、本课教学方法特色
5. **学习目标**：3-8个具体可测量的目标，使用行为动词（如"列举"、"对比"、"设计"、"总结"），避免模糊词汇（如"了解"、"知道"、"掌握"），标注重点和难点。**重要**：学习目标必须以字符串格式输出，每行一个目标，格式如下：
   **注意**：学习目标必须完全基于上传文档的内容，确保涵盖文档中要求的所有知识点和技能。
   ```
   1. 通过朗读课文，能够准确把握文章的感情基调（重点）
   2. 运用批注阅读法，找出并分析文中细节描写的表现手法（难点）
   3. 通过小组合作探究，总结作者情感变化的脉络（重点）
   4. 联系生活实际，写出一篇关于亲情的小片段（难点）
   ```
6. **学习活动**：设计3-8个教学环节，每个环节包含教师活动、学生活动和该环节的具体活动意图。**重要**：每个学习活动都必须包含独立的activity_intent字段，说明该环节的教学意图和目的。**关键要求**：learning_activities中的每个活动必须与lesson_structure中的环节一一对应，确保lesson_structure中提到的每个教学环节（如导入、新知探究、巩固练习、总结与拓展等）都有对应的learning_activity。
   **内容覆盖要求**：每个学习活动都必须明确对应文档中的具体知识点，确保文档中的所有重要内容都在相应的活动中得到教授。
   **内容相符要求**：如果文档中已经包含教学活动建议、教学方法或教学要求，教学设计必须与这些内容相符，并在此基础上进行优化：
     - 保留文档中合理的教学活动设计
     - 改进文档中不够完善的教学方法
     - 增加文档中缺失的思维训练元素
     - 优化文档中的学习活动，使其更符合思维发展型课堂理念
   **知识分离要求**：不同的知识点必须在不同的教学环节中教授，不能将多个知识点混在同一个环节中：
     - 每个环节应该专注于一个核心知识点或技能
     - 复杂知识点可以分解为多个子环节，但每个子环节仍应保持焦点明确
     - 简单相关的知识点可以适当合并，但必须确保每个知识点的教学意图明确
7. **思维训练点**：重点关注认知冲突、思维图示、变式运用三个方面

**注意：**
- 必须严格按照JSON格式输出
- 不要包含任何markdown格式标记
- 不要包含任何解释性文字
- 确保JSON格式正确，可以被解析
- 所有字段都必须填写，不能为空

**最终检查清单：**
在生成教学设计之前，请确保：
1. lesson_structure包含了足够的环节来覆盖文档中的所有知识点
2. 每个learning_activity都有明确的activity_intent，说明如何教授对应的知识内容
3. 学习目标完全基于文档内容，没有遗漏重要知识点
4. 整个教学流程能够完整地教授文档要求的所有内容
5. 不同的知识点在不同的环节中教授，没有混在一起
6. 教学活动设计与文档中的教学要求完全相符，并在基础上进行了优化
7. 如果文档包含教学活动建议，设计中体现并改进了这些建议
8. 所有文档中提到的主要知识点都有对应的专门教学环节

现在请开始分析学习材料并生成教学设计JSON数据："""

    return prompt

def get_json_schema_prompt() -> str:
    """
    获取JSON Schema说明
    
    Returns:
        str: JSON Schema说明
    """
    return """
**JSON Schema 说明：**

必需字段：
- lesson_name: 课例名称
- grade_level: 学段年级  
- subject: 学科
- textbook_version: 教材版本
- lesson_period: 课时说明
- teacher_school: 教师单位
- teacher_name: 教师姓名
- summary: 摘要
- content_analysis: 教学内容分析
- learner_analysis: 学习者分析
- learning_objectives: 学习目标及重难点
- lesson_structure: 课例结构
- learning_activities: 学习活动列表（数组）
- blackboard_design: 板书设计
- homework_extension: 作业与拓展学习设计
- materials_design: 素材设计
- reflection_thinking_points: 思维训练点列表（数组）

learning_activities 数组元素结构：
- name: 活动名称
- teacher_activity: 教师活动
- student_activity: 学生活动
- activity_intent: 活动意图（该环节的教学目的）

reflection_thinking_points 数组元素结构：
- point_type: 思维训练点类型（认知冲突、思维图示、变式运用）
- description: 说明（100字以内）
"""

# 使用示例
if __name__ == "__main__":
    # 测试提示词
    test_user_content = "这是一篇关于春天的散文，描述了春天的美好景象..."
    test_template_content = "教学设计模板内容..."
    
    prompt = get_teaching_design_prompt(test_user_content, test_template_content)
    print("提示词长度:", len(prompt))
    print("提示词预览:")
    print(prompt[:500] + "...")
