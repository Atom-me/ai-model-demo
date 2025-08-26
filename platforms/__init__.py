"""
统一的平台客户端管理
"""
from .qwen import QwenClient
from .openai import OpenAIClient
from .zhipu import ZhipuClient
from .baidu import BaiduClient
from .aihubmix import AIHubMixClient
from .azure import AzureClient

class AIModelManager:
    """AI模型统一管理器"""
    
    def __init__(self):
        self.clients = {}
    
    def get_client(self, platform: str):
        """
        获取指定平台的客户端
        
        Args:
            platform: 平台名称 ('qwen', 'openai', 'zhipu', 'baidu', 'aihubmix', 'azure')
            
        Returns:
            对应平台的客户端实例
        """
        if platform not in self.clients:
            if platform == 'qwen':
                self.clients[platform] = QwenClient()
            elif platform == 'openai':
                self.clients[platform] = OpenAIClient()
            elif platform == 'zhipu':
                self.clients[platform] = ZhipuClient()
            elif platform == 'baidu':
                self.clients[platform] = BaiduClient()
            elif platform == 'aihubmix':
                self.clients[platform] = AIHubMixClient()
            elif platform == 'azure':
                self.clients[platform] = AzureClient()
            else:
                raise ValueError(f"不支持的平台: {platform}")
        
        return self.clients[platform]
    
    def chat(self, platform: str, message: str, **kwargs):
        """
        统一聊天接口
        
        Args:
            platform: 平台名称
            message: 用户消息
            **kwargs: 其他参数
            
        Returns:
            聊天响应
        """
        client = self.get_client(platform)
        return client.chat(message, **kwargs)
    
    def chat_stream(self, platform: str, message: str, **kwargs):
        """
        统一流式聊天接口
        
        Args:
            platform: 平台名称
            message: 用户消息
            **kwargs: 其他参数
            
        Returns:
            流式响应生成器
        """
        client = self.get_client(platform)
        return client.chat_stream(message, **kwargs)

__all__ = [
    'QwenClient', 
    'OpenAIClient', 
    'ZhipuClient', 
    'BaiduClient', 
    'AIHubMixClient',
    'AzureClient',
    'AIModelManager'
]