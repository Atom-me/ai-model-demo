"""
智谱AI API客户端
"""
from zhipuai import ZhipuAI
from typing import Optional, Dict, Any, Generator
from config.config import Config

class ZhipuClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化智谱AI客户端
        
        Args:
            api_key: API密钥，如果不提供则从配置中获取
        """
        self.api_key = api_key or Config.ZHIPU_API_KEY
        
        if not self.api_key:
            raise ValueError("智谱AI API Key未设置")
        
        self.client = ZhipuAI(api_key=self.api_key)
    
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
        model = model or Config.DEFAULT_MODELS['zhipu']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return {
                'success': True,
                'content': response.choices[0].message.content,
                'model': model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                } if response.usage else None
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
        model = model or Config.DEFAULT_MODELS['zhipu']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield {
                        'success': True,
                        'content': chunk.choices[0].delta.content,
                        'model': model
                    }
        except Exception as e:
            yield {
                'success': False,
                'error': str(e)
            }