"""
百度千帆API客户端
"""
import qianfan
from typing import Optional, Dict, Any, Generator
from config.config import Config

class BaiduClient:
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None):
        """
        初始化百度千帆客户端
        
        Args:
            api_key: API密钥，如果不提供则从配置中获取
            secret_key: Secret密钥，如果不提供则从配置中获取
        """
        self.api_key = api_key or Config.BAIDU_API_KEY
        self.secret_key = secret_key or Config.BAIDU_SECRET_KEY
        
        if not self.api_key or not self.secret_key:
            raise ValueError("百度API Key或Secret Key未设置")
        
        # 设置千帆认证信息
        qianfan.ak = self.api_key
        qianfan.sk = self.secret_key
        
        self.chat_comp = qianfan.ChatCompletion()
    
    def chat(self, 
             message: str, 
             model: str = None, 
             temperature: float = 0.7,
             max_tokens: int = 1000,
             system_prompt: str = None,
             **kwargs) -> Dict[str, Any]:
        """
        发送聊天请求
        
        Args:
            message: 用户消息
            model: 模型名称，默认使用配置中的模型
            temperature: 温度参数
            max_tokens: 最大token数量
            system_prompt: 系统提示词
            **kwargs: 其他参数
            
        Returns:
            包含回复和元数据的字典
        """
        model = model or Config.DEFAULT_MODELS['baidu']
        
        messages = []
        if system_prompt:
            messages.append({"role": "user", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.chat_comp.do(
                model=model,
                messages=messages,
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
            
            if response.get('error_code'):
                return {
                    'success': False,
                    'error': response.get('error_msg'),
                    'code': response.get('error_code')
                }
            
            return {
                'success': True,
                'content': response['result'],
                'model': model,
                'usage': response.get('usage')
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
                   system_prompt: str = None,
                   **kwargs) -> Generator[Dict[str, Any], None, None]:
        """
        流式聊天请求
        
        Args:
            message: 用户消息
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数量
            system_prompt: 系统提示词
            **kwargs: 其他参数
            
        Yields:
            流式响应数据
        """
        model = model or Config.DEFAULT_MODELS['baidu']
        
        messages = []
        if system_prompt:
            messages.append({"role": "user", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.chat_comp.do(
                model=model,
                messages=messages,
                temperature=temperature,
                max_output_tokens=max_tokens,
                stream=True,
                **kwargs
            )
            
            for chunk in response:
                if chunk.get('error_code'):
                    yield {
                        'success': False,
                        'error': chunk.get('error_msg'),
                        'code': chunk.get('error_code')
                    }
                    break
                
                if chunk.get('result'):
                    yield {
                        'success': True,
                        'content': chunk['result'],
                        'model': model
                    }
        except Exception as e:
            yield {
                'success': False,
                'error': str(e)
            }