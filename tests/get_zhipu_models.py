"""
查询智谱AI支持的模型列表
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

def get_zhipu_models():
    """查询智谱AI支持的模型"""
    print("🔍 查询智谱AI支持的模型列表")
    print("=" * 60)
    
    if not Config.ZHIPU_API_KEY:
        print("❌ 智谱AI API密钥未配置")
        return
    
    print(f"🔑 API密钥: {Config.ZHIPU_API_KEY[:8]}...")
    print()
    
    try:
        # 智谱AI可能的API端点
        possible_endpoints = [
            "https://open.bigmodel.cn/api/paas/v4/models",
            "https://open.bigmodel.cn/api/v1/models"
        ]
        
        headers = {"Authorization": f"Bearer {Config.ZHIPU_API_KEY}"}
        
        success = False
        for url in possible_endpoints:
            try:
                print(f"📡 尝试调用: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ 查询成功!")
                    
                    if 'data' in data:
                        models = [model['id'] for model in data['data']]
                        print(f"📊 共找到 {len(models)} 个模型:")
                        for i, model in enumerate(sorted(models), 1):
                            print(f"  {i:2d}. {model}")
                    else:
                        print("📋 完整响应数据:")
                        import json
                        print(json.dumps(data, ensure_ascii=False, indent=2))
                    
                    success = True
                    break
                else:
                    print(f"❌ 状态码: {response.status_code}")
                    if response.text:
                        print(f"响应: {response.text[:200]}")
                    
            except Exception as e:
                print(f"❌ 请求异常: {e}")
        
        if not success:
            print("⚠️  API查询失败，列出官方文档中的常用模型:")
            print()
            
            # GLM-4系列
            glm4_models = [
                "glm-4",
                "glm-4v",  
                "glm-4-air",
                "glm-4-airx", 
                "glm-4-long",
                "glm-4-flashx",
                "glm-4-plus",
            ]
            
            # GLM-3系列
            glm3_models = [
                "glm-3-turbo",
            ]
            
            # ChatGLM系列
            chatglm_models = [
                "chatglm_pro", 
                "chatglm_std",
                "chatglm_lite",
                "chatglm_turbo",
            ]
            
            # 多模态模型
            multimodal_models = [
                "cogview-3",
                "cogvlm2-llama3-chat-19b",
            ]
            
            # Embedding模型
            embedding_models = [
                "embedding-2",
            ]
            
            print(f"📂 GLM-4系列 ({len(glm4_models)} 个):")
            for i, model in enumerate(glm4_models, 1):
                print(f"  {i:2d}. {model}")
                
            print(f"\n📂 GLM-3系列 ({len(glm3_models)} 个):")
            for i, model in enumerate(glm3_models, 1):
                print(f"  {i:2d}. {model}")
            
            print(f"\n📂 ChatGLM系列 ({len(chatglm_models)} 个):")
            for i, model in enumerate(chatglm_models, 1):
                print(f"  {i:2d}. {model}")
            
            print(f"\n📂 多模态模型 ({len(multimodal_models)} 个):")
            for i, model in enumerate(multimodal_models, 1):
                print(f"  {i:2d}. {model}")
            
            print(f"\n📂 Embedding模型 ({len(embedding_models)} 个):")
            for i, model in enumerate(embedding_models, 1):
                print(f"  {i:2d}. {model}")
                
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        
    # 显示当前默认模型
    print(f"\n🎯 当前默认模型: {Config.DEFAULT_MODELS['zhipu']}")
    
    # 提供测试建议
    print(f"\n💡 建议测试:")
    print("python tests/test_single_platform.py zhipu -m \"你是什么模型？\"")

if __name__ == "__main__":
    get_zhipu_models()