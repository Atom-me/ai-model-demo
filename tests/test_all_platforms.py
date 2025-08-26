"""
所有平台测试脚本
"""
import os
import sys
import time
from typing import Dict, Any
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from platforms import AIModelManager

# 加载环境变量
load_dotenv()

def test_platform_chat(platform: str, manager: AIModelManager) -> Dict[str, Any]:
    """
    测试单个平台的聊天功能
    
    Args:
        platform: 平台名称
        manager: AI模型管理器
        
    Returns:
        测试结果
    """
    print(f"\n=== 测试 {platform.upper()} 平台 ===")
    
    test_message = "你好，请简单介绍一下你自己。"
    
    try:
        start_time = time.time()
        response = manager.chat(platform, test_message, max_tokens=100)
        end_time = time.time()
        
        if response['success']:
            print(f"✅ {platform} 测试成功")
            print(f"响应时间: {end_time - start_time:.2f}s")
            print(f"模型: {response.get('model', 'Unknown')}")
            print(f"回复: {response['content'][:100]}...")
            
            if response.get('usage'):
                print(f"Token使用: {response['usage']}")
            
            return {
                'platform': platform,
                'success': True,
                'response_time': end_time - start_time,
                'model': response.get('model'),
                'content_length': len(response['content'])
            }
        else:
            print(f"❌ {platform} 测试失败: {response['error']}")
            return {
                'platform': platform,
                'success': False,
                'error': response['error']
            }
    
    except Exception as e:
        print(f"❌ {platform} 测试异常: {str(e)}")
        return {
            'platform': platform,
            'success': False,
            'error': str(e)
        }

def test_platform_stream(platform: str, manager: AIModelManager) -> Dict[str, Any]:
    """
    测试单个平台的流式聊天功能
    
    Args:
        platform: 平台名称
        manager: AI模型管理器
        
    Returns:
        测试结果
    """
    print(f"\n=== 测试 {platform.upper()} 平台流式输出 ===")
    
    test_message = "请用一句话介绍Python编程语言。"
    
    try:
        start_time = time.time()
        full_content = ""
        chunk_count = 0
        
        print("流式输出: ", end="")
        for chunk in manager.chat_stream(platform, test_message, max_tokens=50):
            if chunk['success']:
                content = chunk['content']
                print(content, end="", flush=True)
                full_content += content
                chunk_count += 1
            else:
                print(f"\n❌ 流式输出错误: {chunk['error']}")
                return {
                    'platform': platform,
                    'success': False,
                    'error': chunk['error']
                }
        
        end_time = time.time()
        print(f"\n✅ {platform} 流式测试成功")
        print(f"响应时间: {end_time - start_time:.2f}s")
        print(f"总块数: {chunk_count}")
        
        return {
            'platform': platform,
            'success': True,
            'response_time': end_time - start_time,
            'chunk_count': chunk_count,
            'content_length': len(full_content)
        }
    
    except Exception as e:
        print(f"❌ {platform} 流式测试异常: {str(e)}")
        return {
            'platform': platform,
            'success': False,
            'error': str(e)
        }

def main():
    """主测试函数"""
    print("🚀 开始测试所有AI平台...")
    
    # 支持的平台列表
    platforms = ['qwen', 'openai', 'zhipu', 'baidu', 'aihubmix', 'azure']
    
    # 检查哪些平台有配置的API密钥
    available_platforms = []
    for platform in platforms:
        key_name = f"{platform.upper()}_API_KEY"
        if platform == 'baidu':
            # 百度需要两个密钥
            if os.getenv('BAIDU_API_KEY') and os.getenv('BAIDU_SECRET_KEY'):
                available_platforms.append(platform)
        elif platform == 'azure':
            # Azure需要API密钥和端点
            if os.getenv('AZURE_API_KEY') and os.getenv('AZURE_ENDPOINT'):
                available_platforms.append(platform)
        else:
            if os.getenv(key_name):
                available_platforms.append(platform)
    
    if not available_platforms:
        print("❌ 没有找到任何配置的API密钥，请检查.env文件")
        return
    
    print(f"📋 发现可用平台: {', '.join(available_platforms)}")
    
    manager = AIModelManager()
    
    # 测试结果
    chat_results = []
    stream_results = []
    
    # 测试普通聊天
    print("\n" + "="*50)
    print("测试普通聊天功能")
    print("="*50)
    
    for platform in available_platforms:
        result = test_platform_chat(platform, manager)
        chat_results.append(result)
        time.sleep(1)  # 避免请求过快
    
    # 测试流式聊天
    print("\n" + "="*50)
    print("测试流式聊天功能")
    print("="*50)
    
    for platform in available_platforms:
        result = test_platform_stream(platform, manager)
        stream_results.append(result)
        time.sleep(1)  # 避免请求过快
    
    # 输出总结
    print("\n" + "="*50)
    print("测试结果总结")
    print("="*50)
    
    print("\n普通聊天测试:")
    successful_chat = 0
    for result in chat_results:
        status = "✅" if result['success'] else "❌"
        if result['success']:
            successful_chat += 1
            print(f"{status} {result['platform']}: {result['response_time']:.2f}s")
        else:
            print(f"{status} {result['platform']}: {result['error']}")
    
    print("\n流式聊天测试:")
    successful_stream = 0
    for result in stream_results:
        status = "✅" if result['success'] else "❌"
        if result['success']:
            successful_stream += 1
            print(f"{status} {result['platform']}: {result['response_time']:.2f}s")
        else:
            print(f"{status} {result['platform']}: {result['error']}")
    
    print(f"\n📊 测试完成:")
    print(f"普通聊天: {successful_chat}/{len(available_platforms)} 成功")
    print(f"流式聊天: {successful_stream}/{len(available_platforms)} 成功")

if __name__ == "__main__":
    main()