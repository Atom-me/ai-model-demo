"""
查询Azure OpenAI支持的模型列表
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

def get_azure_models():
    """查询Azure OpenAI支持的模型"""
    print("🔍 查询Azure OpenAI支持的模型列表")
    print("=" * 60)
    
    if not Config.AZURE_API_KEY:
        print("❌ Azure OpenAI API密钥未配置")
        return
        
    if not Config.AZURE_ENDPOINT:
        print("❌ Azure OpenAI Endpoint未配置")
        return
    
    print(f"🔑 API密钥: {Config.AZURE_API_KEY[:8]}...")
    print(f"🌐 端点: {Config.AZURE_ENDPOINT}")
    print(f"📅 API版本: {Config.AZURE_API_VERSION}")
    print()
    
    try:
        # 方法1: 查询可用模型
        # 从聊天端点提取基础端点
        base_endpoint = Config.AZURE_ENDPOINT.split('/openai/deployments')[0]
        models_url = f"{base_endpoint}/openai/models?api-version={Config.AZURE_API_VERSION}"
        headers = {
            "api-key": Config.AZURE_API_KEY,
            "Content-Type": "application/json"
        }
        
        print(f"📡 调用模型列表API: {models_url}")
        print("⏳ 请稍等，正在查询...")
        response = requests.get(models_url, headers=headers, timeout=30)
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                models = data['data']
                print(f"✅ 查询成功，共 {len(models)} 个模型:")
                
                # 按类型分组
                gpt_models = []
                embedding_models = []
                other_models = []
                
                for model in models:
                    model_id = model.get('id', 'Unknown')
                    if 'gpt' in model_id.lower():
                        gpt_models.append(model)
                    elif 'embedding' in model_id.lower() or 'ada' in model_id.lower():
                        embedding_models.append(model)
                    else:
                        other_models.append(model)
                
                if gpt_models:
                    print(f"\n📂 GPT模型 ({len(gpt_models)} 个):")
                    for i, model in enumerate(gpt_models, 1):
                        model_id = model.get('id')
                        created = model.get('created', '')
                        print(f"  {i:2d}. {model_id} (created: {created})")
                
                if embedding_models:
                    print(f"\n📂 Embedding模型 ({len(embedding_models)} 个):")
                    for i, model in enumerate(embedding_models, 1):
                        model_id = model.get('id')
                        created = model.get('created', '')
                        print(f"  {i:2d}. {model_id} (created: {created})")
                
                if other_models:
                    print(f"\n📂 其他模型 ({len(other_models)} 个):")
                    for i, model in enumerate(other_models, 1):
                        model_id = model.get('id')
                        created = model.get('created', '')
                        print(f"  {i:2d}. {model_id} (created: {created})")
                        
            else:
                print("📋 完整响应数据:")
                import json
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
        else:
            print(f"❌ 查询失败: {response.status_code}")
            if response.text:
                print(f"响应内容: {response.text[:300]}")
            
            print("\n💡 可能的原因:")
            print("- API密钥不正确")
            print("- 端点URL格式错误")
            print("- API版本不支持")
            print("- Azure资源未正确配置")
        

    except requests.exceptions.Timeout:
        print(f"❌ 请求超时: Azure服务响应较慢，请检查网络连接或稍后重试")
        print(f"💡 建议: 检查端点URL是否正确: {Config.AZURE_ENDPOINT}")
    except requests.exceptions.ConnectionError:
        print(f"❌ 连接错误: 无法连接到Azure端点")
        print(f"💡 建议: 检查端点URL格式和网络连接")
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        
    # 显示当前默认部署
    print(f"\n🎯 当前默认部署: {Config.DEFAULT_MODELS['azure']}")
    
    # 提供测试建议
    print(f"\n💡 使用建议:")
    print("1. 确保在Azure门户中创建了相应的模型部署")
    print("2. 部署名称需要在代码中使用，不是模型名称")
    print("3. 测试部署: python tests/test_single_platform.py azure -m \"你好\"")
    
    # Azure特殊说明
    print(f"\n📚 Azure OpenAI特殊说明:")
    print("- Azure中使用'部署名称'而不是模型名称")
    print("- 需要在Azure门户中手动创建部署")
    print("- API版本需要与Azure服务兼容")
    print("- 端点格式: https://your-resource-name.openai.azure.com/")

if __name__ == "__main__":
    get_azure_models()