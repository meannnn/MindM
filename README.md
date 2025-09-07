# AI文档助手 - 智能Word文档处理系统

一个基于Python的智能文档处理系统，集成了阿里云百炼大模型API，提供Word文档解析、AI对话、文件上传等功能。

## 🚀 项目概述

本项目是一个完整的AI文档助手解决方案，支持：
- 📄 Word文档智能解析和处理
- 🤖 基于阿里云百炼的AI对话功能
- 📁 文件上传和在线处理
- 🌐 现代化的Web界面
- 🔄 多轮对话和上下文理解

## 📁 项目结构

```
pythondocx/
├── README.md                                    # 项目说明文档
├── requirements.txt                             # Python依赖包
├── .env                                        # 环境变量配置
├── 2023【教学设计模板】思维发展型课堂-XX学校-XX教师.docx  # 示例模板文件
├── web/                                        # Web前端模块
│   ├── templates/                              # HTML模板
│   │   ├── index.html                         # 主页面模板
│   │   └── chat.html                          # 聊天界面模板
│   ├── static/                                # 静态资源
│   │   ├── css/
│   │   │   └── style.css                      # 样式文件
│   │   ├── js/
│   │   │   ├── main.js                        # 主交互逻辑
│   │   │   └── chat.js                        # 聊天功能
│   │   └── templates/
│   │       └── 教学设计模板.docx              # Word模板文件
│   └── README.md                              # Web模块说明
├── docx/                                       # Word文档处理模块
│   ├── __init__.py
│   ├── parsers/                               # 文档解析器
│   │   ├── document_parser.py                 # 主文档解析器
│   │   ├── table_parser.py                    # 表格解析器
│   │   ├── image_parser.py                    # 图片解析器
│   │   └── format_parser.py                   # 格式解析器
│   ├── generators/                            # 文档生成器
│   │   ├── document_generator.py              # 文档生成器
│   │   ├── template_generator.py              # 模板生成器
│   │   ├── table_generator.py                 # 表格生成器
│   │   └── image_generator.py                 # 图片生成器
│   ├── templates/                             # 模板处理
│   │   ├── template_processor.py              # 模板处理器
│   │   ├── placeholder_handler.py             # 占位符处理器
│   │   └── template_validator.py              # 模板验证器
│   ├── utils/                                 # 工具函数
│   │   ├── document_utils.py                  # 文档工具
│   │   ├── format_utils.py                    # 格式工具
│   │   ├── validation_utils.py                # 验证工具
│   │   └── helper_utils.py                    # 辅助工具
│   ├── tests/                                 # 测试文件
│   └── README.md                              # 文档处理模块说明
├── llm/                                       # AI大模型模块
│   ├── __init__.py
│   ├── clients/                               # API客户端
│   │   ├── aliyun_client.py                   # 阿里云百炼客户端
│   │   └── __init__.py
│   └── utils/                                 # 工具函数
│       ├── file_handler.py                    # 文件处理器
│       └── __init__.py
├── uploads/                                   # 上传文件存储目录
├── outputs/                                   # 输出文件存储目录
└── logs/                                      # 日志文件目录
```

## 🛠️ 技术栈

### 后端技术
- **Python 3.8+**: 主要编程语言
- **Flask**: Web框架
- **python-docx**: Word文档处理
- **requests**: HTTP请求库
- **python-dotenv**: 环境变量管理

### 前端技术
- **HTML5**: 现代化页面结构
- **CSS3**: 响应式设计和动画效果
- **JavaScript ES6+**: 交互逻辑和异步处理
- **Font Awesome**: 图标库

### AI服务
- **阿里云百炼**: 大语言模型API
- **OpenAI兼容接口**: 标准化的API调用

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd pythondocx

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件，设置您的API密钥：

```bash
# 阿里云百炼API密钥
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# AI模型配置
DEFAULT_MODEL=qwen-max
TEMPERATURE=0.7
TOP_P=0.8
MAX_TOKENS=2000
```

### 3. 运行应用

```bash
# 启动Web应用
python app.py

# 或者使用启动脚本
python start.py
```

访问 `http://localhost:5000` 开始使用。

## 📖 功能模块详解

### 🌐 Web前端模块 (web/)

现代化的Web界面，提供直观的用户体验：

#### 功能特点
- **🎨 现代化UI设计**: 渐变背景和毛玻璃效果
- **📱 响应式设计**: 支持移动端和桌面端
- **📁 文件上传**: 支持拖拽上传和文件验证
- **💬 聊天界面**: 实时AI对话功能
- **📊 进度显示**: 实时处理状态更新
- **❌ 错误处理**: 友好的错误提示和重试功能

#### 技术特性
- **HTML5**: 语义化标签，现代化结构
- **CSS3**: Flexbox/Grid布局，动画效果
- **JavaScript ES6+**: 模块化编程，异步处理
- **响应式设计**: 支持各种设备尺寸

### 📄 Word文档处理模块 (docx/)

基于python-docx库的完整文档处理解决方案：

#### 核心功能
- **📖 文档解析**: 提取文本、表格、图片、格式信息
- **✍️ 文档生成**: 从零创建或基于模板生成文档
- **🎯 模板处理**: 智能占位符识别和替换
- **🛠️ 工具函数**: 文档验证、内容提取、格式转换

#### 使用示例
```python
from docx.parsers import DocumentParser
from docx.generators import DocumentGenerator
from docx.templates import TemplateProcessor

# 文档解析
parser = DocumentParser("example.docx")
data = parser.parse_document()

# 文档生成
generator = DocumentGenerator()
generator.add_heading("标题", 0)
generator.add_paragraph("内容")
generator.save_document("output.docx")

# 模板处理
processor = TemplateProcessor("template.docx")
processor.fill_template({"title": "新标题"})
processor.save_filled_template("filled.docx")
```

### 🤖 AI大模型模块 (llm/)

集成阿里云百炼API的智能对话功能：

#### 核心功能
- **💬 智能对话**: 支持单轮和多轮对话
- **📁 文件上传**: 支持Word文档上传到云端
- **🔍 文件分析**: 基于上传文件的智能问答
- **⚙️ 参数配置**: 灵活的温度、top_p等参数设置

#### API特性
- **OpenAI兼容**: 使用标准化的API接口
- **多模型支持**: qwen-max, qwen-plus, qwen-turbo等
- **错误处理**: 完善的异常处理和重试机制
- **日志记录**: 详细的操作日志和调试信息

#### 使用示例
```python
from llm.clients import AliyunClient

# 创建客户端
client = AliyunClient()

# 基本对话
result = client.call_model("你好，请介绍一下你自己")
print(result['text'])

# 文件上传和对话
upload_result = client.upload_file("document.docx")
chat_result = client.chat_with_file(
    upload_result['file_id'],
    "这篇文章讲了什么？"
)

# 多轮对话
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"},
    {"role": "user", "content": "请介绍一下AI"}
]
result = client.call_model_with_history(messages)
```

## 🧪 测试和验证

### 运行测试

```bash
# 测试AI API功能
python test_llm_api.py

# 测试Web应用
python test_app.py

# 运行文档处理测试
python -m pytest docx/tests/
```

### 功能验证

1. **API连接测试**: 验证阿里云百炼API连接
2. **文件上传测试**: 测试Word文档上传功能
3. **对话功能测试**: 验证单轮和多轮对话
4. **文档处理测试**: 测试文档解析和生成功能

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
LOG_FILE=./logs/llm.log

# 日志配置
LOG_LEVEL=INFO
ENABLE_FILE_LOGGING=true

# AI模型参数
DEFAULT_MODEL=qwen-max
TEMPERATURE=0.7
TOP_P=0.8
MAX_TOKENS=2000

# 文件上传配置
FILE_PURPOSE=file-extract
SUPPORTED_FILE_TYPES=.docx,.doc,.pdf,.txt
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
- 上传教学文档
- AI分析文档内容
- 自动生成标准化教学设计模板

### 2. 文档智能问答
- 上传Word文档
- 基于文档内容进行问答
- 获取文档摘要和关键信息

### 3. 文档格式转换
- 解析Word文档结构
- 提取文本和表格数据
- 生成新的格式化文档

### 4. 批量文档处理
- 批量上传多个文档
- 自动化内容提取和分析
- 生成处理报告

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

### v0.1.0 (最新)
- ✅ 集成阿里云百炼API
- ✅ 支持OpenAI兼容接口
- ✅ 添加文件上传和对话功能
- ✅ 完善的多轮对话支持
- ✅ 现代化Web界面
- ✅ Word文档处理功能
- ✅ 模板解析和生成
- ✅ 文档格式转换
- ✅ 工具函数集合

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