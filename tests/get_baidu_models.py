"""
查询百度千帆支持的模型列表
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

def get_baidu_models():
    """查询百度千帆支持的模型"""
    print("🔍 查询百度千帆支持的模型列表")
    print("=" * 60)
    
    if not Config.BAIDU_API_KEY or not Config.BAIDU_SECRET_KEY:
        print("❌ 百度千帆API密钥未配置（需要API Key和Secret Key）")
        return
    
    print(f"🔑 API Key: {Config.BAIDU_API_KEY[:8]}...")
    print(f"🔐 Secret Key: {Config.BAIDU_SECRET_KEY[:8]}...")
    print()
    
    try:
        import qianfan
        
        # 设置认证信息
        qianfan.ak = Config.BAIDU_API_KEY
        qianfan.sk = Config.BAIDU_SECRET_KEY
        
        print("📋 百度千帆没有直接的模型列表API，以下是官方支持的常用模型:")
        print()
        
        # 文心大模型系列
        ernie_models = [
            "ernie-4.0-8k",
            "ernie-4.0-turbo-8k",
            "ernie-3.5-8k", 
            "ernie-3.5-4k",
            "ernie-turbo-8k",
            "ernie-bot-turbo",
            "ernie-bot",
            "ernie-bot-4",
            "ernie-speed-128k",
            "ernie-speed-8k",
            "ernie-lite-8k",
            "ernie-tiny-8k",
        ]
        
        # 开源模型
        opensource_models = [
            "llama2-7b-chat",
            "llama2-13b-chat", 
            "llama2-70b-chat",
            "llama3-8b-instruct",
            "llama3-70b-instruct",
            "bloomz-7b1",
            "qianfan-bloomz-7b-compressed",
            "qianfan-chinese-llama2-7b",
            "qianfan-chinese-llama2-13b",
            "chatglm2-6b-32k",
            "aquilachat-7b",
            "xuanyuan-70b-chat",
        ]
        
        # Embedding模型
        embedding_models = [
            "embedding-v1",
            "bge-large-zh",
            "bge-large-en", 
            "tao-8k",
        ]
        
        # 图像生成模型
        image_models = [
            "stable-diffusion-xl",
            "fuyu-8b",
        ]
        
        print(f"📂 文心大模型系列 ({len(ernie_models)} 个):")
        for i, model in enumerate(ernie_models, 1):
            print(f"  {i:2d}. {model}")
            
        print(f"\n📂 开源模型 ({len(opensource_models)} 个):")
        for i, model in enumerate(opensource_models, 1):
            print(f"  {i:2d}. {model}")
        
        print(f"\n📂 Embedding模型 ({len(embedding_models)} 个):")
        for i, model in enumerate(embedding_models, 1):
            print(f"  {i:2d}. {model}")
            
        print(f"\n📂 图像生成模型 ({len(image_models)} 个):")
        for i, model in enumerate(image_models, 1):
            print(f"  {i:2d}. {model}")
        
        # 尝试测试默认模型可用性
        print(f"\n🧪 测试默认模型 '{Config.DEFAULT_MODELS['baidu']}' 可用性...")
        try:
            chat_comp = qianfan.ChatCompletion()
            response = chat_comp.do(
                model=Config.DEFAULT_MODELS['baidu'],
                messages=[{"role": "user", "content": "你好"}],
                max_output_tokens=10
            )
            
            if response.get('error_code'):
                print(f"❌ 默认模型不可用: {response.get('error_msg')}")
            else:
                print(f"✅ 默认模型可用")
                
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            
    except ImportError:
        print("❌ 未安装qianfan包，请运行: uv add qianfan")
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        
    # 显示当前默认模型
    print(f"\n🎯 当前默认模型: {Config.DEFAULT_MODELS['baidu']}")
    
    # 提供测试建议
    print(f"\n💡 建议测试:")
    print("python tests/test_single_platform.py baidu -m \"你好\"")
    
    # 官方文档链接
    print(f"\n📚 官方文档:")
    print("https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t")

if __name__ == "__main__":
    get_baidu_models()