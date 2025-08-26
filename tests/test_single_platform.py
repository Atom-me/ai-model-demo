"""
单个平台测试脚本
"""
import os
import sys
import argparse
import time
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from platforms import AIModelManager

# 加载环境变量
load_dotenv()

def interactive_chat(platform: str):
    """
    交互式聊天测试
    
    Args:
        platform: 平台名称
    """
    print(f"\n🤖 与 {platform.upper()} 开始对话 (输入 'quit' 退出)")
    print("-" * 50)
    
    manager = AIModelManager()
    
    try:
        client = manager.get_client(platform)
        print(f"✅ {platform} 客户端初始化成功")
    except Exception as e:
        print(f"❌ {platform} 客户端初始化失败: {e}")
        return
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见!")
                break
            
            if not user_input:
                continue
            
            print("AI: ", end="", flush=True)
            
            # 选择普通模式还是流式模式
            use_stream = input("\n使用流式输出? (y/n, 默认n): ").lower().strip() == 'y'
            
            if use_stream:
                print("AI: ", end="", flush=True)
                for chunk in manager.chat_stream(platform, user_input):
                    if chunk['success']:
                        print(chunk['content'], end="", flush=True)
                    else:
                        print(f"\n❌ 错误: {chunk['error']}")
                        break
                print()  # 换行
            else:
                start_time = time.time()
                response = manager.chat(platform, user_input)
                end_time = time.time()
                
                if response['success']:
                    print(f"AI: {response['content']}")
                    print(f"\n⏱️  响应时间: {end_time - start_time:.2f}s")
                    if response.get('usage'):
                        print(f"📊 Token使用: {response['usage']}")
                else:
                    print(f"❌ 错误: {response['error']}")
        
        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

def single_test(platform: str, message: str, stream: bool = False):
    """
    单次测试
    
    Args:
        platform: 平台名称
        message: 测试消息
        stream: 是否使用流式输出
    """
    print(f"🧪 测试 {platform.upper()} 平台")
    print(f"📝 消息: {message}")
    print(f"🌊 流式: {'是' if stream else '否'}")
    print("-" * 50)
    
    manager = AIModelManager()
    
    try:
        if stream:
            print("回复: ", end="", flush=True)
            start_time = time.time()
            for chunk in manager.chat_stream(platform, message):
                if chunk['success']:
                    print(chunk['content'], end="", flush=True)
                else:
                    print(f"\n❌ 错误: {chunk['error']}")
                    return
            end_time = time.time()
            print(f"\n⏱️  响应时间: {end_time - start_time:.2f}s")
        else:
            start_time = time.time()
            response = manager.chat(platform, message)
            end_time = time.time()
            
            if response['success']:
                print(f"回复: {response['content']}")
                print(f"\n⏱️  响应时间: {end_time - start_time:.2f}s")
                print(f"🤖 模型: {response.get('model', 'Unknown')}")
                if response.get('usage'):
                    print(f"📊 Token使用: {response['usage']}")
            else:
                print(f"❌ 错误: {response['error']}")
    
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def main():
    parser = argparse.ArgumentParser(description='单个AI平台测试工具')
    parser.add_argument('platform', choices=['qwen', 'openai', 'zhipu', 'baidu', 'aihubmix', 'azure'], 
                       help='选择要测试的平台')
    parser.add_argument('-m', '--message', type=str, 
                       help='测试消息 (如果不提供则进入交互模式)')
    parser.add_argument('-s', '--stream', action='store_true', 
                       help='使用流式输出')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='进入交互模式')
    
    args = parser.parse_args()
    
    # 检查API密钥是否配置
    if args.platform == 'baidu':
        if not (os.getenv('BAIDU_API_KEY') and os.getenv('BAIDU_SECRET_KEY')):
            print(f"❌ {args.platform} 的API密钥未配置，请检查.env文件")
            return
    elif args.platform == 'azure':
        if not (os.getenv('AZURE_API_KEY') and os.getenv('AZURE_ENDPOINT')):
            print(f"❌ {args.platform} 的API密钥和端点未配置，请检查.env文件")
            return
    else:
        key_name = f"{args.platform.upper()}_API_KEY"
        if not os.getenv(key_name):
            print(f"❌ {args.platform} 的API密钥未配置，请检查.env文件")
            return
    
    if args.interactive or not args.message:
        interactive_chat(args.platform)
    else:
        single_test(args.platform, args.message, args.stream)

if __name__ == "__main__":
    main()