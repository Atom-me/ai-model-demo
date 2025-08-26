"""
通过DashScope API查询支持的模型列表
"""
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config

# 加载环境变量
load_dotenv()

def get_supported_models():
    """
    通过DashScope API查询支持的模型列表
    """
    print("🔍 查询通义千问支持的模型列表")
    print("=" * 60)
    
    # 检查API密钥
    if not Config.QWEN_API_KEY:
        print("❌ 通义千问API密钥未配置")
        return
    
    print(f"🔑 API密钥: {Config.QWEN_API_KEY[:8]}...")
    print()
    
    try:
        import dashscope
        from dashscope import Models
        
        # 设置API密钥
        dashscope.api_key = Config.QWEN_API_KEY
        
        print("📋 正在查询模型列表...")
        
        # 调用模型列表API
        response = Models.list()
        
        if hasattr(response, 'status_code') and response.status_code == 200:
            print("✅ 查询成功！")
            print()
            
            if hasattr(response, 'models'):
                models = response.models
                print(f"📊 共找到 {len(models)} 个可用模型：")
                print("-" * 60)
                
                # 按类型分组显示模型
                model_groups = {}
                
                for model in models:
                    model_name = model.model if hasattr(model, 'model') else str(model)
                    
                    # 简单分类
                    if 'qwen-turbo' in model_name or 'qwen-plus' in model_name or 'qwen-max' in model_name:
                        category = "通用模型"
                    elif 'qwen1.5' in model_name:
                        category = "Qwen1.5系列"
                    elif 'qwen2' in model_name:
                        category = "Qwen2系列"
                    elif 'math' in model_name:
                        category = "数学专用"
                    elif 'code' in model_name:
                        category = "代码专用"
                    elif 'long' in model_name:
                        category = "长文本模型"
                    else:
                        category = "其他模型"
                    
                    if category not in model_groups:
                        model_groups[category] = []
                    model_groups[category].append(model_name)
                
                # 分组显示
                for category, model_list in model_groups.items():
                    print(f"\n📂 {category} ({len(model_list)} 个):")
                    for i, model in enumerate(sorted(model_list), 1):
                        print(f"  {i:2d}. {model}")
                
            else:
                print("🔍 响应格式:", response)
                print("\n可用属性:", dir(response))
                
        else:
            print(f"❌ 查询失败")
            print(f"状态码: {getattr(response, 'status_code', 'Unknown')}")
            print(f"错误信息: {getattr(response, 'message', 'Unknown')}")
            
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装 dashscope 包")
        
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        print(f"错误类型: {type(e)}")

def get_models_via_http():
    """
    通过HTTP直接调用DashScope API查询模型列表
    """
    import requests
    
    print("\n" + "=" * 60)
    print("🌐 通过HTTP API查询模型列表")
    print("=" * 60)
    
    if not Config.QWEN_API_KEY:
        print("❌ API密钥未配置")
        return
    
    url = "https://dashscope.aliyuncs.com/api/v1/models"
    headers = {
        "Authorization": f"Bearer {Config.QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("📡 发送HTTP请求...")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 查询成功！")
            print()
            print("📋 响应数据:")
            
            import json
            print(json.dumps(data, ensure_ascii=False, indent=2))
            
        else:
            print(f"❌ HTTP请求失败")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
    except Exception as e:
        print(f"❌ 处理异常: {e}")

if __name__ == "__main__":
    # 方法1: 使用DashScope SDK
    get_supported_models()
    
    # 方法2: 直接HTTP调用
    get_models_via_http()