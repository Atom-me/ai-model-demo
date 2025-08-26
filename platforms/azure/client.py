"""
Azure OpenAI API客户端
"""
from openai import AzureOpenAI
from typing import Optional, Dict, Any, Generator
from config.config import Config

class AzureClient:
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 endpoint: Optional[str] = None,
                 api_version: Optional[str] = None):
        """
        初始化Azure OpenAI客户端
        
        Azure OpenAI Service需要特殊的认证配置：
        - API Key: Azure订阅的API密钥
        - Endpoint: Azure资源的端点URL（格式：https://your-resource-name.openai.azure.com/）
        - API Version: API版本号（如：2024-02-15-preview）
        
        Args:
            api_key: Azure OpenAI API密钥，如果不提供则从配置中获取
            endpoint: Azure OpenAI端点URL，如果不提供则从配置中获取
            api_version: API版本，如果不提供则从配置中获取
        """
        self.api_key = api_key or Config.AZURE_API_KEY
        self.endpoint = endpoint or Config.AZURE_ENDPOINT
        self.api_version = api_version or Config.AZURE_API_VERSION
        
        if not self.api_key:
            raise ValueError("Azure OpenAI API Key未设置")
        if not self.endpoint:
            raise ValueError("Azure OpenAI Endpoint未设置")
        if not self.api_version:
            raise ValueError("Azure OpenAI API Version未设置")
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version
        )
    
    def chat(self, 
             message: str, 
             model: str = None, 
             temperature: float = 0.7,
             max_tokens: int = 1000,
             system_prompt: str = None,
             **kwargs) -> Dict[str, Any]:
        """
        发送聊天请求
        
        注意：Azure OpenAI中的模型名称是部署名称（deployment name），
        不是模型的实际名称。需要在Azure门户中创建部署。
        
        Args:
            message: 用户消息
            model: 部署名称（deployment name），默认使用配置中的部署
            temperature: 温度参数
            max_tokens: 最大token数量
            system_prompt: 系统提示词
            **kwargs: 其他参数
            
        Returns:
            包含回复和元数据的字典
        """
        # Azure中使用部署名称，不是模型名称
        deployment_name = model or Config.DEFAULT_MODELS['azure']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=deployment_name,  # 在Azure中这是部署名称
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return {
                'success': True,
                'content': response.choices[0].message.content,
                'model': deployment_name,
                'deployment_name': deployment_name,
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
            model: 部署名称（deployment name）
            temperature: 温度参数
            max_tokens: 最大token数量
            system_prompt: 系统提示词
            **kwargs: 其他参数
            
        Yields:
            流式响应数据
        """
        deployment_name = model or Config.DEFAULT_MODELS['azure']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            stream = self.client.chat.completions.create(
                model=deployment_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )
            
            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    yield {
                        'success': True,
                        'content': chunk.choices[0].delta.content,
                        'model': deployment_name,
                        'deployment_name': deployment_name
                    }
        except Exception as e:
            yield {
                'success': False,
                'error': str(e)
            }