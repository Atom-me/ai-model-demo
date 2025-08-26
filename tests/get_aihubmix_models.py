"""
查询AIHubMix支持的模型列表
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

def get_aihubmix_models():
    """查询AIHubMix支持的模型"""
    print("🔍 查询AIHubMix支持的模型列表")
    print("=" * 60)
    
    if not Config.AIHUBMIX_API_KEY:
        print("❌ AIHubMix API密钥未配置")
        return
    
    print(f"🔑 API密钥: {Config.AIHUBMIX_API_KEY[:8]}...")
    print(f"🌐 API端点: {Config.AIHUBMIX_BASE_URL}")
    print()
    
    try:
        # AIHubMix通常兼容OpenAI格式
        url = f"{Config.AIHUBMIX_BASE_URL.rstrip('/')}/models"
        headers = {
            "Authorization": f"Bearer {Config.AIHUBMIX_API_KEY}",
            "Content-Type": "application/json"
        }
        
        print(f"📡 调用API: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data and isinstance(data['data'], list):
                models = [model['id'] for model in data['data']]
                print(f"✅ 查询成功，共 {len(models)} 个模型:")
                
                # 按类型分组（基于模型名称）
                gpt_models = [m for m in models if 'gpt' in m.lower()]
                claude_models = [m for m in models if 'claude' in m.lower()]
                gemini_models = [m for m in models if 'gemini' in m.lower()]
                llama_models = [m for m in models if 'llama' in m.lower()]
                other_models = [m for m in models if m not in gpt_models + claude_models + gemini_models + llama_models]
                
                if gpt_models:
                    print(f"\n📂 GPT模型 ({len(gpt_models)} 个):")
                    for i, model in enumerate(sorted(gpt_models), 1):
                        print(f"  {i:2d}. {model}")
                
                if claude_models:
                    print(f"\n📂 Claude模型 ({len(claude_models)} 个):")
                    for i, model in enumerate(sorted(claude_models), 1):
                        print(f"  {i:2d}. {model}")
                
                if gemini_models:
                    print(f"\n📂 Gemini模型 ({len(gemini_models)} 个):")
                    for i, model in enumerate(sorted(gemini_models), 1):
                        print(f"  {i:2d}. {model}")
                
                if llama_models:
                    print(f"\n📂 LLaMA模型 ({len(llama_models)} 个):")
                    for i, model in enumerate(sorted(llama_models), 1):
                        print(f"  {i:2d}. {model}")
                
                if other_models:
                    print(f"\n📂 其他模型 ({len(other_models)} 个):")
                    for i, model in enumerate(sorted(other_models), 1):
                        print(f"  {i:2d}. {model}")
                        
            elif 'models' in data:
                # 兼容其他格式
                models = data['models']
                print(f"✅ 查询成功，共 {len(models)} 个模型:")
                for i, model in enumerate(sorted(models), 1):
                    print(f"  {i:2d}. {model}")
            else:
                print("📋 完整响应数据:")
                import json
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
        elif response.status_code == 401:
            print("❌ 认证失败，请检查API密钥是否正确")
        elif response.status_code == 404:
            print("❌ 端点不存在，AIHubMix可能不支持模型列表API")
            print("💡 显示常见的第三方平台支持的模型:")
            show_common_models()
        else:
            print(f"❌ 查询失败: {response.status_code}")
            if response.text:
                print(f"响应内容: {response.text[:300]}")
            print("💡 显示常见的第三方平台支持的模型:")
            show_common_models()
                
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print("💡 显示常见的第三方平台支持的模型:")
        show_common_models()
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
        print("💡 显示常见的第三方平台支持的模型:")
        show_common_models()
    except Exception as e:
        print(f"❌ 查询异常: {e}")

def show_common_models():
    """显示第三方平台常见的模型"""
    print()
    print("📂 第三方平台常见模型:")
    
    common_models = [
        # GPT系列
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4-32k",
        
        # Claude系列
        "claude-3-sonnet",
        "claude-3-opus",
        "claude-3-haiku",
        "claude-2.1",
        "claude-2",
        "claude-instant-1.2",
        
        # Google系列
        "gemini-pro",
        "gemini-pro-vision", 
        "palm-2",
        
        # 开源模型
        "llama-2-7b-chat",
        "llama-2-13b-chat",
        "llama-2-70b-chat",
        "vicuna-7b",
        "vicuna-13b",
    ]
    
    for i, model in enumerate(common_models, 1):
        print(f"  {i:2d}. {model}")
    
    print(f"\n🎯 当前默认模型: {Config.DEFAULT_MODELS['aihubmix']}")
    
    # 提供测试建议
    print(f"\n💡 建议测试:")
    print("python tests/test_single_platform.py aihubmix -m \"你好\"")

if __name__ == "__main__":
    get_aihubmix_models()