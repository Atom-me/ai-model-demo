"""
查询OpenAI支持的模型列表
"""
import os
import sys
import requests
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config

# 加载环境变量
load_dotenv()

def get_openai_models():
    """查询OpenAI支持的模型"""
    print("🔍 查询OpenAI支持的模型列表")
    print("=" * 60)
    
    if not Config.OPENAI_API_KEY:
        print("❌ OpenAI API密钥未配置")
        return
    
    print(f"🔑 API密钥: {Config.OPENAI_API_KEY[:8]}...")
    print(f"🌐 API端点: {Config.OPENAI_BASE_URL}")
    print()
    
    try:
        # 方法1: 使用OpenAI SDK
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=Config.OPENAI_API_KEY,
                base_url=Config.OPENAI_BASE_URL
            )
            
            print("📡 通过SDK查询...")
            models = client.models.list()
            model_list = [model.id for model in models.data]
            print(f"✅ 查询成功，共 {len(model_list)} 个模型:")
            
            # 按类型分组
            gpt_models = [m for m in model_list if 'gpt' in m.lower()]
            embedding_models = [m for m in model_list if 'embedding' in m.lower() or 'ada' in m.lower()]
            whisper_models = [m for m in model_list if 'whisper' in m.lower()]
            dall_e_models = [m for m in model_list if 'dall' in m.lower()]
            other_models = [m for m in model_list if m not in gpt_models + embedding_models + whisper_models + dall_e_models]
            
            if gpt_models:
                print(f"\n📂 GPT聊天模型 ({len(gpt_models)} 个):")
                for i, model in enumerate(sorted(gpt_models), 1):
                    print(f"  {i:2d}. {model}")
            
            if embedding_models:
                print(f"\n📂 Embedding模型 ({len(embedding_models)} 个):")
                for i, model in enumerate(sorted(embedding_models), 1):
                    print(f"  {i:2d}. {model}")
            
            if whisper_models:
                print(f"\n📂 Whisper语音模型 ({len(whisper_models)} 个):")
                for i, model in enumerate(sorted(whisper_models), 1):
                    print(f"  {i:2d}. {model}")
            
            if dall_e_models:
                print(f"\n📂 DALL-E图像模型 ({len(dall_e_models)} 个):")
                for i, model in enumerate(sorted(dall_e_models), 1):
                    print(f"  {i:2d}. {model}")
            
            if other_models:
                print(f"\n📂 其他模型 ({len(other_models)} 个):")
                for i, model in enumerate(sorted(other_models), 1):
                    print(f"  {i:2d}. {model}")
                    
        except Exception as e:
            print(f"⚠️  SDK方法失败: {e}")
            # 方法2: HTTP直接调用
            print("📡 尝试HTTP调用...")
            
            url = f"{Config.OPENAI_BASE_URL.rstrip('/')}/models"
            headers = {"Authorization": f"Bearer {Config.OPENAI_API_KEY}"}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    models = [model['id'] for model in data['data']]
                    print(f"✅ 通过HTTP查询成功，共 {len(models)} 个模型:")
                    for i, model in enumerate(sorted(models), 1):
                        print(f"  {i:2d}. {model}")
                else:
                    print("📋 响应数据:", data)
            else:
                print(f"❌ HTTP查询失败: {response.status_code}")
                print("响应:", response.text[:200])
                
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        
    # 显示当前默认模型
    print(f"\n🎯 当前默认模型: {Config.DEFAULT_MODELS['openai']}")

if __name__ == "__main__":
    get_openai_models()