"""
通义千问API客户端

使用阿里云DashScope服务，API端点已内置在SDK中：
- HTTP API: https://dashscope.aliyuncs.com/api/v1
- WebSocket API: wss://dashscope.aliyuncs.com/api-ws/v1/inference

内置端点位置: dashscope/common/env.py
- base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
- base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'

可通过环境变量覆盖默认端点：
- DASHSCOPE_HTTP_BASE_URL: 自定义HTTP API端点
- DASHSCOPE_WEBSOCKET_BASE_URL: 自定义WebSocket API端点
- DASHSCOPE_API_REGION: API区域 (默认: cn-beijing)
- DASHSCOPE_API_VERSION: API版本 (默认: v1)
"""
import dashscope
from dashscope import Generation
from typing import Optional, Dict, Any
from config.config import Config

class QwenClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化通义千问客户端
        
        注意：通义千问只需要API密钥，不需要配置API端点URL
        因为DashScope SDK已经内置了阿里云官方API端点
        
        Args:
            api_key: API密钥，如果不提供则从配置中获取
                    可从阿里云DashScope控制台获取：https://dashscope.console.aliyun.com/
        """
        self.api_key = api_key or Config.QWEN_API_KEY
        # 设置全局API密钥，DashScope SDK会自动使用内置的API端点
        dashscope.api_key = self.api_key
    
    def chat(self, 
             message: str, 
             model: str = None, 
             temperature: float = 0.7,
             max_tokens: int = 1000,
             **kwargs) -> Dict[str, Any]:
        """
        发送聊天请求
        
        Args:
            message: 用户消息
            model: 模型名称，默认使用配置中的模型
            temperature: 温度参数
            max_tokens: 最大token数量
            **kwargs: 其他参数
            
        Returns:
            包含回复和元数据的字典
        """
        if not self.api_key:
            raise ValueError("API Key未设置")
        
        model = model or Config.DEFAULT_MODELS['qwen']
        
        try:
            # 调用DashScope Generation API
            # 内部会自动发送请求到: https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
            response = Generation.call(
                model=model,
                prompt=message,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'content': response.output.text,
                    'model': model,
                    'usage': response.usage if hasattr(response, 'usage') else None
                }
            else:
                return {
                    'success': False,
                    'error': response.message,
                    'code': response.code
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def chat_stream(self, 
                   message: str, 
                   model: str = None, 
                   temperature: float = 0.7,
                   max_tokens: int = 1000,
                   **kwargs):
        """
        流式聊天请求
        
        Args:
            message: 用户消息
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数量
            **kwargs: 其他参数
            
        Yields:
            流式响应数据
        """
        if not self.api_key:
            raise ValueError("API Key未设置")
        
        model = model or Config.DEFAULT_MODELS['qwen']
        
        try:
            # 流式调用DashScope Generation API
            # 内部会自动连接到WebSocket端点: wss://dashscope.aliyuncs.com/api-ws/v1/inference
            responses = Generation.call(
                model=model,
                prompt=message,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,  # 启用流式输出
                **kwargs
            )
            
            for response in responses:
                if response.status_code == 200:
                    yield {
                        'success': True,
                        'content': response.output.text,
                        'model': model
                    }
                else:
                    yield {
                        'success': False,
                        'error': response.message,
                        'code': response.code
                    }
                    break
        except Exception as e:
            yield {
                'success': False,
                'error': str(e)
            }