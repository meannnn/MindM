"""
阿里云百炼API客户端

基于阿里云百炼API实现的大语言模型客户端，支持直接调用大模型进行对话。
"""

import os
import logging
import requests
import json
from typing import Dict, List, Any, Optional, Union
from http import HTTPStatus
from datetime import datetime

logger = logging.getLogger(__name__)


class AliyunClient:
    """阿里云百炼API客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化阿里云客户端
        
        Args:
            api_key: 阿里云API密钥，如果不提供则从环境变量获取
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        
        if not self.api_key:
            raise ValueError("API Key未提供，请设置DASHSCOPE_API_KEY环境变量或传入api_key参数")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
        
        logger.info("阿里云百炼客户端初始化完成")
    
    def call_model(self, prompt: str, model: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        直接调用大模型进行对话
        
        Args:
            prompt: 输入提示词
            model: 模型名称，默认为qwen-max
            parameters: 额外参数
            
        Returns:
            Dict[str, Any]: API响应结果
        """
        try:
            # 使用环境变量中的默认模型
            if model is None:
                model = os.getenv("DEFAULT_MODEL", "qwen-max")
            
            # 使用OpenAI兼容接口
            url = f"{self.base_url}/chat/completions"
            
            # 构建请求数据，使用OpenAI兼容格式
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "top_p": float(os.getenv("TOP_P", "0.8")),
                "max_tokens": int(os.getenv("MAX_TOKENS", "2000")),
                **(parameters or {})
            }
            
            logger.info(f"调用阿里云大模型API: {url}")
            logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 发送请求
            response = self.session.post(url, json=data, timeout=60)
            
            # 处理响应
            if response.status_code == HTTPStatus.OK:
                result = response.json()
                logger.info("API调用成功")
                logger.debug(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
                
                # 提取响应内容（OpenAI兼容格式）
                choices = result.get('choices', [])
                if choices and len(choices) > 0:
                    text = choices[0].get('message', {}).get('content', '')
                else:
                    text = ''
                
                return {
                    'success': True,
                    'data': result,
                    'request_id': result.get('id'),
                    'text': text,
                    'usage': result.get('usage', {}),
                    'model': result.get('model', model)
                }
            else:
                # 处理错误响应
                try:
                    error_data = response.json()
                    error_message = error_data.get('message', response.text)
                except:
                    error_message = response.text
                
                error_info = {
                    'success': False,
                    'status_code': response.status_code,
                    'message': error_message,
                    'request_id': response.headers.get('X-Request-Id')
                }
                logger.error(f"API调用失败: {error_info}")
                return error_info
                
        except requests.exceptions.Timeout:
            error_info = {
                'success': False,
                'error': 'timeout',
                'message': '请求超时，请稍后重试'
            }
            logger.error("API调用超时")
            return error_info
            
        except requests.exceptions.RequestException as e:
            error_info = {
                'success': False,
                'error': 'request_error',
                'message': f'网络请求失败: {str(e)}'
            }
            logger.error(f"API请求异常: {e}")
            return error_info
            
        except Exception as e:
            error_info = {
                'success': False,
                'error': 'unknown_error',
                'message': f'未知错误: {str(e)}'
            }
            logger.error(f"未知错误: {e}")
            return error_info

    def call_model_with_history(self, messages: List[Dict[str, str]], model: Optional[str] = None, 
                               parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        支持多轮对话的模型调用
        
        Args:
            messages: 对话历史，格式为 [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
            model: 模型名称
            parameters: 额外参数
            
        Returns:
            Dict[str, Any]: API响应结果
        """
        try:
            # 使用环境变量中的默认模型
            if model is None:
                model = os.getenv("DEFAULT_MODEL", "qwen-max")
            
            # 使用OpenAI兼容接口
            url = f"{self.base_url}/chat/completions"
            
            # 构建请求数据（OpenAI兼容格式）
            data = {
                "model": model,
                "messages": messages,
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "top_p": float(os.getenv("TOP_P", "0.8")),
                "max_tokens": int(os.getenv("MAX_TOKENS", "2000")),
                **(parameters or {})
            }
            
            logger.info(f"调用阿里云大模型API（多轮对话）: {url}")
            logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 发送请求
            response = self.session.post(url, json=data, timeout=60)
            
            # 处理响应（OpenAI兼容格式）
            if response.status_code == HTTPStatus.OK:
                result = response.json()
                logger.info("API调用成功")
                
                # 提取响应内容（OpenAI兼容格式）
                choices = result.get('choices', [])
                if choices and len(choices) > 0:
                    text = choices[0].get('message', {}).get('content', '')
                else:
                    text = ''
                
                return {
                    'success': True,
                    'data': result,
                    'request_id': result.get('id'),
                    'text': text,
                    'usage': result.get('usage', {}),
                    'model': result.get('model', model)
                }
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get('message', response.text)
                except:
                    error_message = response.text
                
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'message': error_message,
                    'request_id': response.headers.get('X-Request-Id')
                }
                
        except Exception as e:
            logger.error(f"多轮对话调用失败: {e}")
            return {
                'success': False,
                'error': 'unknown_error',
                'message': str(e)
            }

    def upload_file(self, file_path: str, purpose: str = "file-extract") -> Dict[str, Any]:
        """
        上传文件到阿里云百炼
        
        Args:
            file_path: 文件路径
            purpose: 文件用途，默认为"file-extract"
            
        Returns:
            Dict[str, Any]: 上传结果
        """
        try:
            url = f"{self.base_url}/files"
            
            # 准备文件上传
            with open(file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(file_path), f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                }
                data = {
                    'purpose': purpose
                }
                
                # 移除Content-Type头，让requests自动设置multipart/form-data
                headers = {
                    'Authorization': f'Bearer {self.api_key}'
                }
                
                response = requests.post(url, files=files, data=data, headers=headers, timeout=60)
            
            if response.status_code == HTTPStatus.OK:
                result = response.json()
                return {
                    'success': True,
                    'file_id': result.get('id'),
                    'filename': result.get('filename'),
                    'purpose': result.get('purpose'),
                    'size': result.get('bytes'),
                    'data': result
                }
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get('message', response.text)
                except:
                    error_message = response.text
                
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'message': error_message
                }
                
        except Exception as e:
            logger.error(f"文件上传失败: {e}")
            return {
                'success': False,
                'error': 'upload_failed',
                'message': str(e)
            }
    
    def chat_with_file(self, file_id: str, user_message: str, model: Optional[str] = None) -> Dict[str, Any]:
        """
        使用文件进行对话
        
        Args:
            file_id: 上传文件的ID
            user_message: 用户消息
            model: 模型名称
            
        Returns:
            Dict[str, Any]: 对话结果
        """
        try:
            if model is None:
                model = os.getenv("DEFAULT_MODEL", "qwen-max")
            
            url = f"{self.base_url}/chat/completions"
            
            # 构建请求数据
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": f"fileid://{file_id}"
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "top_p": float(os.getenv("TOP_P", "0.8")),
                "max_tokens": int(os.getenv("MAX_TOKENS", "2000"))
            }
            
            response = self.session.post(url, json=data, timeout=60)
            
            if response.status_code == HTTPStatus.OK:
                result = response.json()
                
                choices = result.get('choices', [])
                if choices and len(choices) > 0:
                    text = choices[0].get('message', {}).get('content', '')
                else:
                    text = ''
                
                return {
                    'success': True,
                    'data': result,
                    'request_id': result.get('id'),
                    'text': text,
                    'usage': result.get('usage', {}),
                    'model': result.get('model', model)
                }
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get('message', response.text)
                except:
                    error_message = response.text
                
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'message': error_message
                }
                
        except Exception as e:
            logger.error(f"文件对话失败: {e}")
            return {
                'success': False,
                'error': 'chat_failed',
                'message': str(e)
            }

    def get_usage_info(self) -> Dict[str, Any]:
        """
        获取API使用信息
        
        Returns:
            Dict[str, Any]: 使用信息
        """
        return {
            'api_key': self.api_key[:10] + "..." if self.api_key else None,
            'base_url': self.base_url
        }


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建客户端
    client = AliyunClient()
    
    # 测试基本调用
    result = client.call_model("你好，请介绍一下你自己")
    
    if result['success']:
        print(f"API调用成功: {result['text']}")
    else:
        print(f"API调用失败: {result['message']}")