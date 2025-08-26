"""
AIHubMix API客户端 (兼容OpenAI格式)
"""
from openai import OpenAI
from typing import Optional, Dict, Any, Generator
from config.config import Config

class AIHubMixClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化AIHubMix客户端
        
        Args:
            api_key: API密钥，如果不提供则从配置中获取
            base_url: API基础URL，如果不提供则从配置中获取
        """
        self.api_key = api_key or Config.AIHUBMIX_API_KEY
        self.base_url = base_url or Config.AIHUBMIX_BASE_URL
        
        if not self.api_key:
            raise ValueError("AIHubMix API Key未设置")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat(self, 
             message: str, 
             model: str = None, 
             temperature: float = 0.7,
             max_tokens: int = 1000,
             max_completion_tokens: int = None,
             system_prompt: str = None,
             **kwargs) -> Dict[str, Any]:
        """
        发送聊天请求
        
        Args:
            message: 用户消息
            model: 模型名称，默认使用配置中的模型
            temperature: 温度参数
            max_tokens: 最大token数量 (兼容旧模型)
            max_completion_tokens: 最大完成token数量 (新模型如GPT-5)
            system_prompt: 系统提示词
            **kwargs: 其他参数
            
        Returns:
            包含回复和元数据的字典
        """
        model = model or Config.DEFAULT_MODELS['aihubmix']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        # 智能选择token参数：GPT-5等新模型使用max_completion_tokens，其他使用max_tokens
        token_params = {}
        if max_completion_tokens is not None:
            # 优先使用max_completion_tokens (适用于GPT-5等新模型)
            token_params['max_completion_tokens'] = max_completion_tokens
        elif 'gpt-5' in model.lower() or 'o1' in model.lower():
            # 如果是新模型但没有指定max_completion_tokens，则使用max_tokens的值
            token_params['max_completion_tokens'] = max_tokens
        else:
            # 其他模型使用传统的max_tokens参数
            token_params['max_tokens'] = max_tokens
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                **token_params,
                **kwargs
            )
            
            # 获取响应内容，处理可能的None值
            content = response.choices[0].message.content or ""
            
            return {
                'success': True,
                'content': content,
                'model': model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                } if response.usage else None,
                'raw_response': response  # 添加原始响应用于调试
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
                   max_completion_tokens: int = None,
                   system_prompt: str = None,
                   **kwargs) -> Generator[Dict[str, Any], None, None]:
        """
        流式聊天请求
        
        Args:
            message: 用户消息
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数量 (兼容旧模型)
            max_completion_tokens: 最大完成token数量 (新模型如GPT-5)
            system_prompt: 系统提示词
            **kwargs: 其他参数
            
        Yields:
            流式响应数据
        """
        model = model or Config.DEFAULT_MODELS['aihubmix']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        # 智能选择token参数
        token_params = {}
        if max_completion_tokens is not None:
            token_params['max_completion_tokens'] = max_completion_tokens
        elif 'gpt-5' in model.lower() or 'o1' in model.lower():
            token_params['max_completion_tokens'] = max_tokens
        else:
            token_params['max_tokens'] = max_tokens
        
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True,
                **token_params,
                **kwargs
            )
            
            for chunk in stream:
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