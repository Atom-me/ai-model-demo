"""
配置文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    
    # 通义千问 (DashScope)
    # 注意：通义千问不需要配置API URL，因为DashScope SDK内置了端点
    # API端点已内置: https://dashscope.aliyuncs.com/api/v1
    QWEN_API_KEY = os.getenv('QWEN_API_KEY')
    
    # 智谱AI
    # 注意：智谱AI也不需要配置API URL，SDK内置了端点
    ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY')
    
    # 百度千帆
    # 注意：百度千帆也不需要配置API URL，SDK内置了端点
    # 需要API Key和Secret Key两个密钥
    BAIDU_API_KEY = os.getenv('BAIDU_API_KEY')
    BAIDU_SECRET_KEY = os.getenv('BAIDU_SECRET_KEY')
    
    # AIHubMix (第三方平台)
    # 注意：第三方平台需要配置API URL，因为端点不固定
    AIHUBMIX_API_KEY = os.getenv('AIHUBMIX_API_KEY')
    AIHUBMIX_BASE_URL = os.getenv('AIHUBMIX_BASE_URL', 'https://aihubmix.com/v1')
    
    # Azure OpenAI (微软云平台)
    # 注意：Azure OpenAI需要特殊配置
    # - API Key: Azure订阅的API密钥
    # - Endpoint: Azure资源端点 (https://your-resource-name.openai.azure.com/)
    # - API Version: API版本 (如: 2024-02-15-preview)
    AZURE_API_KEY = os.getenv('AZURE_API_KEY')
    AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
    AZURE_API_VERSION = os.getenv('AZURE_API_VERSION', '2024-08-01-preview')
    
    # 默认模型配置
    DEFAULT_MODELS = {
        'openai': 'gpt-4o',  # 使用最新的GPT-4o模型
        'qwen': 'qwen-turbo',
        'zhipu': 'glm-4',
        'baidu': 'ernie-bot-turbo',
        'aihubmix': 'gpt-4o',  # AIHubMix也使用GPT-4o
        'azure': 'gpt-4o-deployment'  # Azure中是部署名称，需要在Azure门户中创建
    }