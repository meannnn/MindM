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
        上传文件到阿里云百炼（使用OpenAI兼容接口）
        
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

    def upload_file_with_openai_client(self, file_path: str) -> Dict[str, Any]:
        """
        使用OpenAI客户端上传文件到阿里云百炼
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 上传结果
        """
        try:
            from openai import OpenAI
            from pathlib import Path
            
            # 创建OpenAI客户端
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            # 上传文件
            file_object = client.files.create(
                file=Path(file_path), 
                purpose="file-extract"
            )
            
            return {
                'success': True,
                'file_id': file_object.id,
                'filename': file_object.filename,
                'purpose': file_object.purpose,
                'size': file_object.bytes,
                'created_at': file_object.created_at,
                'data': file_object
            }
            
        except Exception as e:
            logger.error(f"OpenAI客户端文件上传失败: {e}")
            return {
                'success': False,
                'error': 'openai_upload_failed',
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

    def chat_with_qwen_long_and_files(self, user_file_id: str, template_file_id: str, 
                                     model: str = "qwen-long") -> Dict[str, Any]:
        """
        使用Qwen-Long模型和两个文件进行教学设计生成
        
        Args:
            user_file_id: 用户上传文件的ID
            template_file_id: 模板文件的ID
            model: 模型名称，默认为qwen-long
            
        Returns:
            Dict[str, Any]: 对话结果
        """
        try:
            # 构建包含两个文件ID的提示词
            prompt = """好的，这是为您转换成中文的提示词。

---

### **中文提示词：**

**角色：** 您是一位精通教学法和课程设计的专家。

**任务：** 基于"思维发展型课堂"模型，根据用户提供的学习材料，创建一份全面、高质量的教学设计。

**输入：**
1. 一份由用户上传的，包含特定课程学习材料的Word文档。
2. 一份固定的教学设计模板（即先前您学习过的模板）。

**核心指令：**
您的目标是仔细分析学习材料，并为模板中的**每一个板块**生成相关、创新且符合教学原理的内容。最终的输出必须严格遵守模板的结构；不得增加、删除或调整任何板块的顺序。模板中原有的所有标题和表格都必须完整地保留在您的最终输出中。

**各板块内容生成指南：**

1. **表头信息（`课例名称`、`学段年级`等）**
   * **`课例名称`**：使用所提供学习材料的标题或核心主题。
   * **`学段年级`**：根据材料内容的复杂程度，推断出最合适的学段年级（例如：小学一年级，初中二年级）。
   * **`学科`**：识别出对应的学科（例如：语文、数学、历史）。
   * **`教材版本`**：填写"根据所给材料"或在可能的情况下进行推断。
   * **`课时说明`**：将本教案设计为1个课时（填写"第1课时"）。
   * **`教师单位`**和**`教师姓名`**：保留为"XX学校"和"XX教师"。

2. **【摘要】**
   * 撰写一段300-500字的概括。首先，从材料中提炼课程的核心主题和目标。简要描述该主题的传统教学方法及其潜在的"痛点"（尤其是在核心素养培养方面）。然后，介绍您为本课设计的具体教学方法，阐述它将如何实现学习目标，以及它期望体现的特色（例如：注重探究、使用思维工具、合作学习等）。

3. **【教学内容分析】**
   * 分析所提供的文本。阐明其核心知识点和技能要求，并将其置于更广泛的课程体系中，解释它与学生先前所学和未来将学内容的联系。

4. **【学习者分析】**
   * 根据您所识别的学段年级，描述目标学生的典型特征。分析他们与本课主题相关的已有知识水平、认知发展阶段和学习特点。

5. **【学习目标及重难点】**
   * 制定3-4个具体、可测量、可达成的学习目标。
   * 遵循模板附录中简化的ABCD模式。每个目标都应清晰地说明学生在课后能够**做什么**。
   * 请使用具体的行为动词（如："列举"、"对比"、"设计"、"总结"），避免使用模糊的词汇（如："了解"、"知道"、"掌握"）。
   * 在每个目标后，将主要学习目标标注为**（重点）**，将最具挑战性的目标标注为**（难点）**。

6. **【课例结构】**
   * 呈现您教学设计的整体结构和流程。可以使用文本格式，如编号列表或简单的流程图来概述主要阶段（例如：`导入 -> 新知探究 -> 巩固练习 -> 总结与拓展`）。

7. **【学习活动设计】**
   * 这是您任务的核心部分。设计一个详尽的、分步骤的教学过程。
   * 创建几个清晰的"环节"，例如导入、主要活动、小组讨论和总结。
   * 对于每个环节，填写表格，详细描述"教师活动"和相应的"学生活动"。
   * 在每个环节的表格后，撰写清晰的"活动意图说明"，解释该环节的教学目的，以及它如何帮助学生达成学习目标。

8. **【板书设计】**
   * 用文本格式描述您将如何设计板书。使用标题和要点来展示在课程中，关键术语、图示和总结将被书写在黑板的哪个位置。

9. **【作业与拓展学习设计】**
   * 设计一到两个家庭作业或一项拓展学习活动，以巩固课上所学内容并鼓励学生进一步思考。

10. **【素材设计】**
    * 保留此标题。如果您构思了具体的学习单或练习纸，请简要描述其组成部分或问题。如果不需要额外材料，请直接陈述"本课未设计额外学习素材"。

11. **【反思：思维训练点】**
    * 回顾您刚刚创建的教学设计，并填写所提供的表格。
    * **`认知冲突`**：在您的教学设计中，找出1-2个学生可能会遇到挑战性或反直觉观点的地方，这些地方能促使他们进行批判性思考。
    * **`思维图示`**：找出1-2个在您的课程中使用了思维工具（如思维导图、流程图、对比图）的实例。
    * **`变式运用`**：找出1-2个您通过变化的练习或案例来深化学生理解的例子。
    * 在"说明"栏中，为每个要点提供简短的解释（100字以内）。

---
**最终指令：**
现在，请开始分析用户上传的Word文档学习材料，并严格按照以上所有指南，生成一份完整的教学设计。"""

            url = f"{self.base_url}/chat/completions"
            
            # 构建请求数据，使用两个文件ID
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "system",
                        "content": f"fileid://{user_file_id}"
                    },
                    {
                        "role": "system", 
                        "content": f"fileid://{template_file_id}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "top_p": float(os.getenv("TOP_P", "0.8")),
                "max_tokens": int(os.getenv("MAX_TOKENS", "4000")),
                "stream": True,
                "stream_options": {
                    "include_usage": True
                }
            }
            
            logger.info(f"调用Qwen-Long模型API（双文件模式）: {url}")
            logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 发送请求
            response = self.session.post(url, json=data, timeout=120, stream=True)
            
            # 处理流式响应
            if response.status_code == HTTPStatus.OK:
                full_content = ""
                usage_info = {}
                
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]
                            if data_str.strip() == '[DONE]':
                                break
                            try:
                                chunk_data = json.loads(data_str)
                                if chunk_data.get('choices') and chunk_data['choices'][0].get('delta', {}).get('content'):
                                    full_content += chunk_data['choices'][0]['delta']['content']
                                if chunk_data.get('usage'):
                                    usage_info = chunk_data['usage']
                            except json.JSONDecodeError:
                                continue
                
                return {
                    'success': True,
                    'text': full_content,
                    'usage': usage_info,
                    'model': model,
                    'request_id': response.headers.get('X-Request-Id')
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
            logger.error(f"Qwen-Long双文件模式调用失败: {e}")
            return {
                'success': False,
                'error': 'unknown_error',
                'message': str(e)
            }

    def call_model_with_files(self, user_file_content: str, template_file_content: str, 
                             model: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        使用用户文件和模板文件内容调用大模型
        
        Args:
            user_file_content: 用户上传文件的文本内容
            template_file_content: 模板文件的文本内容
            model: 模型名称
            parameters: 额外参数
            
        Returns:
            Dict[str, Any]: API响应结果
        """
        try:
            # 使用环境变量中的默认模型
            if model is None:
                model = os.getenv("DEFAULT_MODEL", "qwen-max")
            
            # 构建包含两个文件内容的提示词
            prompt = f"""好的，这是为您转换成中文的提示词。

---

### **中文提示词：**

**角色：** 您是一位精通教学法和课程设计的专家。

**任务：** 基于"思维发展型课堂"模型，根据用户提供的学习材料，创建一份全面、高质量的教学设计。

**输入：**
1. 一份由用户上传的，包含特定课程学习材料的Word文档。
2. 一份固定的教学设计模板（即先前您学习过的模板）。

**核心指令：**
您的目标是仔细分析学习材料，并为模板中的**每一个板块**生成相关、创新且符合教学原理的内容。最终的输出必须严格遵守模板的结构；不得增加、删除或调整任何板块的顺序。模板中原有的所有标题和表格都必须完整地保留在您的最终输出中。

**各板块内容生成指南：**

1. **表头信息（`课例名称`、`学段年级`等）**
   * **`课例名称`**：使用所提供学习材料的标题或核心主题。
   * **`学段年级`**：根据材料内容的复杂程度，推断出最合适的学段年级（例如：小学一年级，初中二年级）。
   * **`学科`**：识别出对应的学科（例如：语文、数学、历史）。
   * **`教材版本`**：填写"根据所给材料"或在可能的情况下进行推断。
   * **`课时说明`**：将本教案设计为1个课时（填写"第1课时"）。
   * **`教师单位`**和**`教师姓名`**：保留为"XX学校"和"XX教师"。

2. **【摘要】**
   * 撰写一段300-500字的概括。首先，从材料中提炼课程的核心主题和目标。简要描述该主题的传统教学方法及其潜在的"痛点"（尤其是在核心素养培养方面）。然后，介绍您为本课设计的具体教学方法，阐述它将如何实现学习目标，以及它期望体现的特色（例如：注重探究、使用思维工具、合作学习等）。

3. **【教学内容分析】**
   * 分析所提供的文本。阐明其核心知识点和技能要求，并将其置于更广泛的课程体系中，解释它与学生先前所学和未来将学内容的联系。

4. **【学习者分析】**
   * 根据您所识别的学段年级，描述目标学生的典型特征。分析他们与本课主题相关的已有知识水平、认知发展阶段和学习特点。

5. **【学习目标及重难点】**
   * 制定3-4个具体、可测量、可达成的学习目标。
   * 遵循模板附录中简化的ABCD模式。每个目标都应清晰地说明学生在课后能够**做什么**。
   * 请使用具体的行为动词（如："列举"、"对比"、"设计"、"总结"），避免使用模糊的词汇（如："了解"、"知道"、"掌握"）。
   * 在每个目标后，将主要学习目标标注为**（重点）**，将最具挑战性的目标标注为**（难点）**。

6. **【课例结构】**
   * 呈现您教学设计的整体结构和流程。可以使用文本格式，如编号列表或简单的流程图来概述主要阶段（例如：`导入 -> 新知探究 -> 巩固练习 -> 总结与拓展`）。

7. **【学习活动设计】**
   * 这是您任务的核心部分。设计一个详尽的、分步骤的教学过程。
   * 创建几个清晰的"环节"，例如导入、主要活动、小组讨论和总结。
   * 对于每个环节，填写表格，详细描述"教师活动"和相应的"学生活动"。
   * 在每个环节的表格后，撰写清晰的"活动意图说明"，解释该环节的教学目的，以及它如何帮助学生达成学习目标。

8. **【板书设计】**
   * 用文本格式描述您将如何设计板书。使用标题和要点来展示在课程中，关键术语、图示和总结将被书写在黑板的哪个位置。

9. **【作业与拓展学习设计】**
   * 设计一到两个家庭作业或一项拓展学习活动，以巩固课上所学内容并鼓励学生进一步思考。

10. **【素材设计】**
    * 保留此标题。如果您构思了具体的学习单或练习纸，请简要描述其组成部分或问题。如果不需要额外材料，请直接陈述"本课未设计额外学习素材"。

11. **【反思：思维训练点】**
    * 回顾您刚刚创建的教学设计，并填写所提供的表格。
    * **`认知冲突`**：在您的教学设计中，找出1-2个学生可能会遇到挑战性或反直觉观点的地方，这些地方能促使他们进行批判性思考。
    * **`思维图示`**：找出1-2个在您的课程中使用了思维工具（如思维导图、流程图、对比图）的实例。
    * **`变式运用`**：找出1-2个您通过变化的练习或案例来深化学生理解的例子。
    * 在"说明"栏中，为每个要点提供简短的解释（100字以内）。

---
**最终指令：**
现在，请开始分析用户上传的Word文档学习材料，并严格按照以上所有指南，生成一份完整的教学设计。

---

**用户上传的学习材料内容：**
{user_file_content}

---

**教学设计模板内容：**
{template_file_content}"""

            # 使用OpenAI兼容接口
            url = f"{self.base_url}/chat/completions"
            
            # 构建请求数据
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
                "max_tokens": int(os.getenv("MAX_TOKENS", "4000")),  # 增加token限制以支持更长的输出
                **(parameters or {})
            }
            
            logger.info(f"调用阿里云大模型API（双文件模式）: {url}")
            logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 发送请求
            response = self.session.post(url, json=data, timeout=120)  # 增加超时时间
            
            # 处理响应
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
            logger.error(f"双文件模式调用失败: {e}")
            return {
                'success': False,
                'error': 'unknown_error',
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