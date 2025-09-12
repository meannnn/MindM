# AI教学设计生成器 - 基于docxtpl的智能文档处理系统

一个基于Python的智能教学设计生成系统，集成了阿里云百炼大模型API和docxtpl模板引擎，提供Word文档解析、AI分析、模板填充等功能。

## 🚀 项目概述

本项目是一个完整的AI教学设计生成解决方案，支持：
- 📄 Word文档智能解析和处理
- 🤖 基于阿里云百炼的AI内容分析
- 📝 使用docxtpl进行模板填充
- 🎯 多种教学设计模板支持
- 🌐 现代化的Web界面
- 📊 实时处理状态显示

## 📁 项目结构

```
pythondocx/
├── README.md                                    # 项目说明文档
├── README_DOCXTPL.md                           # docxtpl使用说明
├── CHANGELOG.md                                # 版本更新日志
├── requirements.txt                             # Python依赖包
├── app.py                                      # 主应用文件
├── start.py                                    # 启动脚本
├── start.bat                                   # Windows启动脚本
├── 2023【教学设计模板】思维发展型课堂-XX学校-XX教师.docx  # 示例模板文件
├── web/                                        # Web前端模块
│   ├── templates/                              # HTML模板
│   │   ├── index.html                         # 主页面模板
│   │   └── chat.html                          # 聊天界面模板
│   └── static/                                # 静态资源
│       ├── css/
│       │   └── style.css                      # 样式文件
│       ├── js/
│       │   ├── main.js                        # 主交互逻辑
│       │   └── chat.js                        # 聊天功能
│       └── templates/
│           └── 教学设计模板.docx              # Word模板文件
├── docx_processor/                             # 文档处理模块
│   ├── __init__.py
│   ├── template_processor.py                  # docxtpl模板处理器
│   ├── parsers/                               # 文档解析器
│   │   ├── document_parser.py                 # 主文档解析器
│   │   ├── table_parser.py                    # 表格解析器
│   │   ├── image_parser.py                    # 图片解析器
│   │   └── format_parser.py                   # 格式解析器
│   ├── generators/                            # 文档生成器
│   │   └── document_generator.py              # 文档生成器
│   ├── templates/                             # 模板处理
│   │   └── template_processor.py              # 模板处理器
│   ├── utils/                                 # 工具函数
│   │   └── document_utils.py                  # 文档工具
│   └── tests/                                 # 测试文件
│       └── test_docx_module.py                # 模块测试
├── llm/                                       # AI大模型模块
│   ├── __init__.py
│   ├── clients/                               # API客户端
│   │   ├── aliyun_client.py                   # 阿里云百炼客户端
│   │   └── __init__.py
│   └── utils/                                 # 工具函数
│       ├── file_handler.py                    # 文件处理器
│       └── __init__.py
├── prompts/                                   # 提示词模块
│   └── teaching_design_prompt.py              # 教学设计提示词
├── schemas/                                   # 数据模型
│   └── teaching_design_schema.py              # 教学设计数据模型
├── templates/                                 # Word模板文件
│   ├── teaching_design_template.docx          # 基础教学设计模板
│   ├── table_teaching_design_template.docx    # 表格式教学设计模板
│   ├── advanced_table_teaching_design_template.docx  # 高级表格式模板
│   ├── docxtpl_table_teaching_design_template.docx   # docxtpl表格式模板
│   └── optimized_teaching_design_template.docx       # 优化教学设计模板
├── uploads/                                   # 上传文件存储目录
├── outputs/                                   # 输出文件存储目录
└── logs/                                      # 日志文件目录
```

## 🛠️ 技术栈

### 后端技术
- **Python 3.8+**: 主要编程语言
- **Flask**: Web框架
- **python-docx**: Word文档处理
- **docxtpl**: Word模板填充引擎
- **requests**: HTTP请求库
- **python-dotenv**: 环境变量管理
- **Pydantic**: 数据验证和序列化

### 前端技术
- **HTML5**: 现代化页面结构
- **CSS3**: 响应式设计和动画效果
- **JavaScript ES6+**: 交互逻辑和异步处理
- **Font Awesome**: 图标库

### AI服务
- **阿里云百炼**: 大语言模型API
- **OpenAI兼容接口**: 标准化的API调用

### 模板引擎
- **docxtpl**: 基于Jinja2的Word模板填充
- **Jinja2**: 模板语法引擎

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>

# 创建虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件，设置您的API密钥：

```bash
# 阿里云百炼API密钥
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# AI模型配置
DEFAULT_MODEL=qwen-long
TEMPERATURE=0.7
TOP_P=0.8
MAX_TOKENS=4000

# 应用配置
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

### 3. 运行应用

```bash
# 启动Web应用
python app.py

# 或者使用启动脚本
python start.py

# Windows用户可以使用批处理文件
start.bat
```

访问 `http://localhost:5000` 开始使用。

## 🎯 核心功能

### 1. 教学设计生成
- **文档上传**: 支持Word文档上传
- **AI分析**: 使用阿里云百炼分析文档内容
- **模板填充**: 基于docxtpl自动填充教学设计模板
- **多模板支持**: 提供多种教学设计模板选择
- **实时处理**: 显示处理进度和状态

### 2. 模板系统
- **基础模板**: 标准教学设计模板
- **表格式模板**: 支持表格形式的学习活动设计
- **高级模板**: 包含更多细节的完整模板
- **自定义模板**: 支持用户自定义模板

### 3. 数据验证
- **JSON Schema**: 使用Pydantic进行数据验证
- **格式转换**: 自动转换AI输出格式
- **错误处理**: 完善的错误提示和重试机制

## 📖 功能模块详解

### 🌐 Web前端模块 (web/)

现代化的Web界面，提供直观的用户体验：

#### 功能特点
- **🎨 现代化UI设计**: 渐变背景和毛玻璃效果
- **📱 响应式设计**: 支持移动端和桌面端
- **📁 文件上传**: 支持拖拽上传和文件验证
- **📊 进度显示**: 实时处理状态更新
- **❌ 错误处理**: 友好的错误提示和重试功能
- **📝 模板选择**: 支持多种教学设计模板选择

#### 技术特性
- **HTML5**: 语义化标签，现代化结构
- **CSS3**: Flexbox/Grid布局，动画效果
- **JavaScript ES6+**: 模块化编程，异步处理
- **响应式设计**: 支持各种设备尺寸

### 📄 文档处理模块 (docx_processor/)

基于python-docx和docxtpl的完整文档处理解决方案：

#### 核心功能
- **📖 文档解析**: 提取文本、表格、图片、格式信息
- **✍️ 模板填充**: 使用docxtpl进行智能模板填充
- **🎯 数据转换**: 将AI输出转换为模板所需格式
- **🛠️ 工具函数**: 文档验证、内容提取、格式转换

#### 使用示例
```python
from docx_processor.template_processor import TemplateProcessor
from schemas.teaching_design_schema import TeachingDesignData

# 创建模板处理器
processor = TemplateProcessor("templates/teaching_design_template.docx")

# 准备数据
data = TeachingDesignData(
    title="教学设计",
    subject="语文",
    grade="八年级",
    # ... 其他字段
)

# 填充模板
processor.fill_template(data)
processor.save_filled_template("output.docx")
```

### 🤖 AI大模型模块 (llm/)

集成阿里云百炼API的智能文档分析功能：

#### 核心功能
- **📁 文件上传**: 支持Word文档上传到云端
- **🔍 文档分析**: 基于上传文件的智能内容分析
- **📝 教学设计生成**: 自动生成结构化教学设计内容
- **⚙️ 参数配置**: 灵活的温度、top_p等参数设置

#### API特性
- **OpenAI兼容**: 使用标准化的API接口
- **多模型支持**: qwen-max, qwen-plus, qwen-turbo, qwen-long等
- **错误处理**: 完善的异常处理和重试机制
- **日志记录**: 详细的操作日志和调试信息

#### 使用示例
```python
from llm.clients.aliyun_client import AliyunClient
from prompts.teaching_design_prompt import get_teaching_design_prompt

# 创建客户端
client = AliyunClient()

# 上传文件
upload_result = client.upload_file("document.docx")

# 生成教学设计
prompt = get_teaching_design_prompt()
result = client.call_model_with_file(
    upload_result['file_id'],
    prompt
)

# 解析结果
from schemas.teaching_design_schema import validate_teaching_design_data
design_data = validate_teaching_design_data(result['text'])
```

## 🧪 测试和验证

### 运行测试

```bash
# 测试文档处理模块
python -m pytest docx_processor/tests/

# 测试AI API功能
python -c "from llm.clients.aliyun_client import AliyunClient; print('API连接正常')"

# 测试模板处理
python -c "from docx_processor.template_processor import TemplateProcessor; print('模板处理器正常')"
```

### 功能验证

1. **API连接测试**: 验证阿里云百炼API连接
2. **文件上传测试**: 测试Word文档上传功能
3. **模板填充测试**: 验证docxtpl模板填充功能
4. **数据验证测试**: 测试Pydantic数据模型验证

## ⚙️ 配置说明

### 环境变量配置 (.env)

```bash
# 阿里云百炼API配置
DASHSCOPE_API_KEY=your_api_key_here

# API请求配置
API_TIMEOUT=60
MAX_RETRIES=3

# 目录配置
DEFAULT_OUTPUT_DIR=./outputs
LOG_FILE=./logs/app.log

# 日志配置
LOG_LEVEL=INFO
ENABLE_FILE_LOGGING=true

# AI模型参数
DEFAULT_MODEL=qwen-long
TEMPERATURE=0.7
TOP_P=0.8
MAX_TOKENS=4000

# 文件上传配置
FILE_PURPOSE=file-extract
SUPPORTED_FILE_TYPES=.docx,.doc
```

### 模型参数说明

- **DEFAULT_MODEL**: 默认使用的AI模型
  - `qwen-max`: 最强性能模型
  - `qwen-plus`: 平衡性能和速度
  - `qwen-turbo`: 快速响应模型
  - `qwen-long`: 长文本处理模型

- **TEMPERATURE**: 控制回答的随机性 (0.0-1.0)
- **TOP_P**: 控制回答的多样性 (0.0-1.0)
- **MAX_TOKENS**: 最大生成token数

## 🔧 开发和部署

### 开发环境

```bash
# 安装开发依赖
pip install -r requirements.txt

# 启动开发服务器
python app.py

# 启用调试模式
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### 生产部署

```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 使用Docker部署
docker build -t ai-doc-assistant .
docker run -p 5000:5000 ai-doc-assistant
```

## 📝 使用场景

### 1. 教学设计模板生成
- 上传教学文档（课文、教案等）
- AI分析文档内容，提取关键信息
- 自动生成标准化教学设计模板
- 支持多种模板格式选择

### 2. 教学内容结构化
- 将非结构化教学内容转换为结构化格式
- 自动提取学习目标、重难点、活动设计等
- 生成符合教学标准的文档

### 3. 教学资源整理
- 批量处理教学文档
- 统一格式和结构
- 提高教学准备效率

### 4. 教学评估和反馈
- 基于教学内容生成评估标准
- 提供教学改进建议
- 支持教学反思和总结

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   ```
   错误: API Key未提供
   解决: 检查.env文件中的DASHSCOPE_API_KEY设置
   ```

2. **文件上传失败**
   ```
   错误: 文件上传失败
   解决: 检查文件格式和大小限制
   ```

3. **模型调用超时**
   ```
   错误: 请求超时
   解决: 增加API_TIMEOUT设置或检查网络连接
   ```

### 日志查看

```bash
# 查看应用日志
tail -f logs/llm.log

# 查看错误日志
grep "ERROR" logs/llm.log
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License

## 🔄 更新日志

### v0.2.0 (最新)
- ✅ 集成docxtpl模板引擎
- ✅ 支持多种教学设计模板
- ✅ 添加Pydantic数据验证
- ✅ 优化AI提示词和输出格式
- ✅ 支持表格式学习活动设计
- ✅ 完善的前端模板选择功能
- ✅ 清理无用测试文件
- ✅ 优化文档结构和说明

### v0.1.0
- ✅ 集成阿里云百炼API
- ✅ 支持OpenAI兼容接口
- ✅ 添加文件上传和AI分析功能
- ✅ 现代化Web界面
- ✅ Word文档处理功能
- ✅ 基础模板解析和生成

### v0.0.1
- ✅ 项目初始化和架构设计
- ✅ 技术方案和需求分析
- ✅ 基础项目结构搭建

## 📞 支持

如有问题或建议，请通过以下方式联系：

- 📧 邮箱: [your-email@example.com]
- 🐛 Issues: [GitHub Issues]
- 📖 文档: [项目文档链接]

---

**AI文档助手** - 让文档处理更智能，让AI对话更便捷！