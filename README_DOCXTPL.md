# 基于docxtpl的教学设计生成系统

## 项目概述

本项目使用docxtpl库实现了将LLM返回的数据写入Word模板的功能，创建了一个完整的教学设计生成系统。系统能够：

1. 用户上传Word文档
2. LLM分析文档内容
3. 将分析结果填入Word模板，生成标准化的教学设计文档

## 功能特点

- ✅ **docxtpl集成**：使用docxtpl库实现模板填充功能
- ✅ **JSON格式约束**：设计JSON Schema约束LLM输出格式
- ✅ **阿里云大模型**：连接真实的阿里云百炼API
- ✅ **Word模板**：创建包含占位符的Word模板
- ✅ **完整工作流**：上传→分析→生成→下载的完整流程
- ✅ **Web界面**：提供友好的Web操作界面

## 系统架构

```
用户上传文档 → 文件处理 → LLM分析 → JSON验证 → 模板填充 → 生成Word文档
     ↓              ↓         ↓         ↓         ↓           ↓
  Web界面 → FileHandler → AliyunClient → Schema → DocxTpl → 下载
```

## 核心组件

### 1. 模板处理器 (TemplateProcessor)
- 位置：`docx_processor/template_processor.py`
- 功能：使用docxtpl将JSON数据填入Word模板
- 特点：支持复杂的数据结构，包括列表和嵌套对象

### 2. JSON Schema验证
- 位置：`schemas/teaching_design_schema.py`
- 功能：定义和验证教学设计数据的JSON格式
- 特点：确保LLM输出的数据格式正确

### 3. 提示词生成
- 位置：`prompts/teaching_design_prompt.py`
- 功能：生成引导LLM输出JSON格式的提示词
- 特点：详细的格式要求和示例

### 4. Word模板
- 位置：`templates/teaching_design_template.docx`
- 功能：包含占位符的Word模板文件
- 特点：使用Jinja2语法，支持复杂的数据填充

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
创建`.env`文件：
```env
DASHSCOPE_API_KEY=your_aliyun_api_key
DEFAULT_MODEL=qwen-max
TEMPERATURE=0.7
TOP_P=0.8
MAX_TOKENS=4000
```

### 3. 启动应用
```bash
python app.py
```

### 4. 访问Web界面
打开浏览器访问：`http://localhost:5000`

## 使用流程

1. **上传文档**：在Web界面上传Word文档
2. **自动处理**：系统自动分析文档内容
3. **LLM生成**：调用阿里云大模型生成教学设计JSON
4. **模板填充**：使用docxtpl将数据填入Word模板
5. **下载结果**：下载生成的教学设计Word文档

## API接口

### 1. 文件上传
```
POST /upload
Content-Type: multipart/form-data

参数：
- file: Word文档文件
- template: 模板类型
- ai_model: AI模型选择
```

### 2. 生成教学设计
```
POST /generate_teaching_design
Content-Type: application/json

参数：
- file_id: 上传文件的ID
```

### 3. 下载结果
```
GET /download_design/{file_id}
```

## JSON数据格式

教学设计数据采用以下JSON格式：

```json
{
    "lesson_name": "课例名称",
    "grade_level": "学段年级",
    "subject": "学科",
    "textbook_version": "教材版本",
    "lesson_period": "课时说明",
    "teacher_school": "教师单位",
    "teacher_name": "教师姓名",
    "summary": "摘要",
    "content_analysis": "教学内容分析",
    "learner_analysis": "学习者分析",
    "learning_objectives": "学习目标及重难点",
    "lesson_structure": "课例结构",
    "learning_activities": [
        {
            "name": "活动名称",
            "teacher_activity": "教师活动",
            "student_activity": "学生活动"
        }
    ],
    "activity_intent": "活动意图说明",
    "blackboard_design": "板书设计",
    "homework_extension": "作业与拓展学习设计",
    "materials_design": "素材设计",
    "reflection_thinking_points": [
        {
            "point_type": "思维训练点类型",
            "description": "说明"
        }
    ]
}
```

## 技术栈

- **后端**：Flask + Python
- **文档处理**：python-docx + docxtpl
- **AI模型**：阿里云百炼API
- **前端**：HTML + CSS + JavaScript
- **模板引擎**：Jinja2 (docxtpl内置)

## 文件结构

```
pythondocx/
├── app.py                          # 主应用文件
├── requirements.txt                # 依赖列表
├── templates/
│   └── teaching_design_template.docx  # Word模板
├── schemas/
│   └── teaching_design_schema.py      # JSON Schema定义
├── prompts/
│   └── teaching_design_prompt.py      # 提示词生成
├── docx_processor/
│   └── template_processor.py          # 模板处理器
├── llm/
│   ├── clients/
│   │   └── aliyun_client.py           # 阿里云客户端
│   └── utils/
│       └── file_handler.py            # 文件处理
└── web/
    ├── templates/
    │   └── index.html                 # Web界面
    └── static/
        ├── css/
        │   └── style.css              # 样式文件
        └── js/
            └── main.js                # JavaScript文件
```

## 测试

运行测试脚本：
```bash
python test_simple.py
```

测试包括：
- JSON Schema验证
- 提示词生成
- 模板处理器
- 完整工作流程

## 注意事项

1. **API密钥**：需要配置有效的阿里云百炼API密钥
2. **文件格式**：目前只支持.docx格式的Word文档
3. **文件大小**：限制上传文件大小为10MB
4. **模板路径**：确保模板文件路径正确
5. **依赖版本**：确保所有依赖库版本兼容

## 扩展功能

可以进一步扩展的功能：
- 支持更多文档格式（PDF、TXT等）
- 添加更多教学设计模板
- 支持批量处理
- 添加用户认证系统
- 集成更多AI模型

## 故障排除

### 常见问题

1. **模板加载失败**：检查模板文件路径和权限
2. **LLM调用失败**：检查API密钥和网络连接
3. **JSON解析错误**：检查LLM输出格式
4. **文件生成失败**：检查输出目录权限

### 日志查看

查看应用日志：
```bash
tail -f logs/app.log
```

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目采用MIT许可证。
