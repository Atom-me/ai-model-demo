"""
AI模型对接Demo主程序
"""
import os
import sys
from dotenv import load_dotenv
from platforms import AIModelManager

def main():
    """主程序"""
    load_dotenv()
    
    print("🚀 AI模型对接Demo")
    print("支持平台: OpenAI, 通义千问, 智谱AI, 百度千帆, AIHubMix, Azure OpenAI")
    print("-" * 50)
    
    # 检查可用平台
    platforms = ['qwen', 'openai', 'zhipu', 'baidu', 'aihubmix', 'azure']
    available_platforms = []
    
    for platform in platforms:
        if platform == 'baidu':
            if os.getenv('BAIDU_API_KEY') and os.getenv('BAIDU_SECRET_KEY'):
                available_platforms.append(platform)
        elif platform == 'azure':
            if os.getenv('AZURE_API_KEY') and os.getenv('AZURE_ENDPOINT'):
                available_platforms.append(platform)
        else:
            key_name = f"{platform.upper()}_API_KEY"
            if os.getenv(key_name):
                available_platforms.append(platform)
    
    if not available_platforms:
        print("❌ 没有找到任何配置的API密钥")
        print("请复制 .env.example 为 .env 并配置API密钥")
        return
    
    print(f"✅ 可用平台: {', '.join(available_platforms)}")
    
    # 简单示例
    manager = AIModelManager()
    
    print("\n📝 运行示例测试...")
    
    for platform in available_platforms[:2]:  # 只测试前两个平台
        try:
            print(f"\n测试 {platform}...")
            response = manager.chat(platform, "你好，请简单介绍一下你自己", max_tokens=50)
            if response['success']:
                print(f"✅ {platform}: {response['content'][:100]}...")
            else:
                print(f"❌ {platform}: {response['error']}")
        except Exception as e:
            print(f"❌ {platform}: {e}")
    
    print("\n🔧 使用方法:")
    print("1. 运行完整测试: python tests/test_all_platforms.py")
    print("2. 单平台测试: python tests/test_single_platform.py <platform>")
    print("3. 交互模式: python tests/test_single_platform.py <platform> -i")

if __name__ == "__main__":
    main()
