#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文档助手 - 主应用文件
基于Flask的Web应用，集成阿里云百炼API和Word文档处理功能
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入自定义模块
try:
    from llm.clients.aliyun_client import AliyunClient
    from llm.utils.file_handler import FileHandler
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保llm模块已正确安装")
    sys.exit(1)

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.getenv("LOG_FILE", "./logs/app.log"), encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__, 
           template_folder='web/templates',
           static_folder='web/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 初始化组件
try:
    llm_client = AliyunClient()
    file_handler = FileHandler()
    logger.info("组件初始化成功")
except Exception as e:
    logger.error(f"组件初始化失败: {e}")
    sys.exit(1)

# 存储文件信息的简单内存存储（生产环境应使用数据库）
uploaded_files = {}

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """聊天界面"""
    return render_template('chat.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """文件上传接口"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '没有选择文件'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': '没有选择文件'})
        
        # 保存文件
        result = file_handler.save_uploaded_file(file)
        
        if result['success']:
            file_id = result['file_id']
            uploaded_files[file_id] = result
            
            # 提取文本内容
            text_result = file_handler.extract_text_from_docx(result['file_path'])
            if text_result['success']:
                uploaded_files[file_id]['text_content'] = text_result['text_content']
            
            return jsonify({
                'success': True,
                'file_id': file_id,
                'filename': result['original_filename'],
                'file_size': result['file_size']
            })
        else:
            return jsonify({'success': False, 'error': result['message']})
            
    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/send_message', methods=['POST'])
def send_message():
    """发送消息接口"""
    try:
        data = request.get_json()
        message = data.get('message')
        file_id = data.get('file_id')
        conversation_history = data.get('history', [])
        
        if not message:
            return jsonify({'success': False, 'error': '消息不能为空'})
        
        # 获取文件信息
        file_info = None
        if file_id and file_id in uploaded_files:
            file_info = uploaded_files[file_id]
        
        # 构建提示词
        prompt_content = message
        if file_info and file_info.get('text_content'):
            prompt_content = f"以下是文件内容：\n{file_info['text_content']}\n\n我的问题是：{message}"
        
        # 调用AI模型
        if conversation_history:
            # 构建完整的对话历史
            messages = []
            for msg in conversation_history:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
            # 添加当前消息
            messages.append({
                "role": "user",
                "content": prompt_content
            })
            result = llm_client.call_model_with_history(messages)
        else:
            result = llm_client.call_model(prompt_content)
        
        if result['success']:
            return jsonify({
                'success': True,
                'response': result['text'],
                'request_id': result.get('request_id'),
                'usage': result.get('usage')
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('message', 'AI处理失败'),
                'status_code': result.get('status_code')
            })
            
    except Exception as e:
        logger.error(f"发送消息失败: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_file_content/<file_id>')
def get_file_content(file_id):
    """获取文件内容"""
    try:
        if file_id not in uploaded_files:
            return jsonify({'success': False, 'error': '文件不存在'})
        
        file_info = uploaded_files[file_id]
        return jsonify({
            'success': True,
            'filename': file_info['original_filename'],
            'text_content': file_info.get('text_content', ''),
            'file_size': file_info['file_size']
        })
        
    except Exception as e:
        logger.error(f"获取文件内容失败: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/favicon.ico')
def favicon():
    """网站图标"""
    return send_file('web/static/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/health')
def health():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '0.1.0'
    })

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': '页面不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"内部服务器错误: {error}")
    return jsonify({'error': '内部服务器错误'}), 500

if __name__ == '__main__':
    # 确保必要的目录存在
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # 启动应用
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"启动AI文档助手，端口: {port}, 调试模式: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )