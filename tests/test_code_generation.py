"""
AIHubMix代码生成测试脚本
"""
import os
import sys
import time
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from platforms.aihubmix import AIHubMixClient
from config.config import Config

# 加载环境变量
load_dotenv()

def test_code_generation():
    """测试AIHubMix代码生成功能"""
    print("🚀 AIHubMix代码生成测试")
    print("=" * 60)
    
    if not Config.AIHUBMIX_API_KEY:
        print("❌ AIHubMix API密钥未配置")
        return
    
    print(f"🔑 API密钥: {Config.AIHUBMIX_API_KEY[:8]}...")
    print(f"🌐 API端点: {Config.AIHUBMIX_BASE_URL}")
    print()
    
    try:
        # 初始化客户端
        client = AIHubMixClient()
        print("✅ AIHubMix客户端初始化成功")
        print()
        
        # 代码生成测试用例 - 只测试Vue.js登录表单
        test_cases = [
            {
                "name": "Vue.js登录表单",
                "prompt": """使用Vue.js创建一个简单的登录表单，要求如下：
1. 包含用户名和密码输入框
2. 包含登录按钮
3. 添加基本的表单验证（用户名不能为空，密码长度至少6位）
4. 验证失败时显示错误提示
5. 登录成功时显示成功消息
6. 使用Vue 3的组合式API
7. 包含基本的CSS样式""",
                "max_tokens": 1500
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"📝 测试 {i}: {test_case['name']}")
            print(f"💭 提示: {test_case['prompt'][:50]}...")
            print(f"🎯 最大tokens: {test_case['max_tokens']}")
            
            try:
                # 发送代码生成请求 - 可以尝试不同模型
                # 可选模型: "gpt-5", "gpt-4o", "gpt-4-turbo", "claude-3-sonnet"
                model_to_use = "gpt-4o"  # 先尝试gpt-4o，如果需要GPT-5再改回来
                
                print(f"🤖 使用模型: {model_to_use}")
                
                start_time = time.time()
                
                response = client.chat(
                    message=test_case['prompt'],
                    model=model_to_use,
                    max_tokens=test_case['max_tokens'],  # gpt-4o使用max_tokens
                    temperature=0.2,  # 代码生成使用较低温度以确保准确性
                    system_prompt="你是一个专业的前端开发工程师，精通Vue.js。请生成高质量、可运行的代码，包含适当的注释。代码应该遵循Vue.js最佳实践。"
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                if response['success']:
                    print(f"✅ 生成成功 - 响应时间: {response_time:.2f}s")
                    
                    # 检查内容长度
                    content = response.get('content', '')
                    if not content or content.strip() == '':
                        print("⚠️  警告: 响应内容为空！")
                        print("🔍 调试信息:")
                        
                        # 显示原始响应调试信息
                        if 'raw_response' in response:
                            raw_resp = response['raw_response']
                            print(f"  - 响应对象类型: {type(raw_resp)}")
                            print(f"  - Choices数量: {len(raw_resp.choices) if hasattr(raw_resp, 'choices') else 'N/A'}")
                            
                            if hasattr(raw_resp, 'choices') and raw_resp.choices:
                                choice = raw_resp.choices[0]
                                print(f"  - Message类型: {type(choice.message) if hasattr(choice, 'message') else 'N/A'}")
                                print(f"  - Message内容: '{choice.message.content}'" if hasattr(choice, 'message') else 'N/A')
                                print(f"  - Finish reason: {choice.finish_reason}" if hasattr(choice, 'finish_reason') else 'N/A')
                        
                        print("💡 可能的原因:")
                        print("  1. GPT-5模型可能需要不同的参数配置")
                        print("  2. 请求被内容过滤器拦截")
                        print("  3. API返回格式发生变化")
                        print("  4. 模型正在处理中但未完成")
                    else:
                        # 显示完整的生成代码
                        print(f"📄 完整生成代码:")
                        print("=" * 60)
                        print(response['content'])
                        print("=" * 60)
                    
                    # 显示使用情况
                    if response.get('usage'):
                        usage = response['usage']
                        print(f"📊 Token使用: 输入={usage.get('prompt_tokens', 'N/A')}, "
                              f"输出={usage.get('completion_tokens', 'N/A')}, "
                              f"总计={usage.get('total_tokens', 'N/A')}")
                    
                    results.append({
                        'name': test_case['name'],
                        'success': True,
                        'response_time': response_time,
                        'content_length': len(response['content']),
                        'usage': response.get('usage'),
                        'model_used': model_to_use
                    })
                    
                else:
                    print(f"❌ 生成失败: {response['error']}")
                    results.append({
                        'name': test_case['name'],
                        'success': False,
                        'error': response['error'],
                        'model_used': model_to_use
                    })
                
            except Exception as e:
                print(f"❌ 测试异常: {str(e)}")
                results.append({
                    'name': test_case['name'],
                    'success': False,
                    'error': str(e),
                    'model_used': model_to_use if 'model_to_use' in locals() else 'Unknown'
                })
            
            print()
            
            # 避免请求过快
            if i < len(test_cases):
                time.sleep(1)
        
        # 显示测试总结
        print("=" * 60)
        print("📊 测试结果总结")
        print("=" * 60)
        
        successful_tests = [r for r in results if r['success']]
        failed_tests = [r for r in results if not r['success']]
        
        print(f"\n✅ 成功测试: {len(successful_tests)}/{len(test_cases)}")
        for result in successful_tests:
            print(f"  📝 {result['name']}: {result.get('model_used', 'Unknown')} - "
                  f"{result['response_time']:.2f}s, {result['content_length']} 字符")
        
        if failed_tests:
            print(f"\n❌ 失败测试: {len(failed_tests)}")
            for result in failed_tests:
                print(f"  📝 {result['name']}: {result.get('model_used', 'Unknown')} - {result['error']}")
        
        if successful_tests:
            avg_time = sum(r['response_time'] for r in successful_tests) / len(successful_tests)
            avg_length = sum(r['content_length'] for r in successful_tests) / len(successful_tests)
            print(f"\n📈 平均响应时间: {avg_time:.2f}s")
            print(f"📏 平均代码长度: {avg_length:.0f} 字符")
        
        print(f"\n💡 代码生成建议:")
        print("- 使用较低的temperature (0.1-0.3) 确保代码准确性")
        print("- 根据代码复杂度调整max_tokens (500-2000)")
        print("- 添加system_prompt指定代码风格和要求")
        print("- 对于复杂功能，可以分步骤生成")
        
    except Exception as e:
        print(f"❌ 客户端初始化或测试异常: {e}")

def interactive_code_generation():
    """交互式代码生成"""
    print("\n" + "=" * 60)
    print("🎯 交互式代码生成模式")
    print("=" * 60)
    print("输入代码需求，AI将为你生成代码")
    print("输入 'quit' 退出\n")
    
    if not Config.AIHUBMIX_API_KEY:
        print("❌ AIHubMix API密钥未配置")
        return
    
    try:
        client = AIHubMixClient()
        
        while True:
            try:
                user_input = input("👨‍💻 请描述你需要的代码: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再见!")
                    break
                
                if not user_input:
                    continue
                
                # 获取代码类型和复杂度
                print("\n🔧 代码生成配置:")
                
                # 选择最大tokens
                print("选择代码复杂度:")
                print("1. 简单 (500 tokens) - 简单函数或代码片段")
                print("2. 中等 (1000 tokens) - 完整功能模块")
                print("3. 复杂 (2000 tokens) - 复杂算法或多个类")
                
                complexity = input("请选择 (1-3, 默认2): ").strip()
                
                max_tokens_map = {'1': 500, '2': 1000, '3': 2000}
                max_tokens = max_tokens_map.get(complexity, 1000)
                
                print(f"\n🚀 正在生成代码... (最大tokens: {max_tokens})")
                
                start_time = time.time()
                response = client.chat(
                    message=user_input,
                    max_tokens=max_tokens,
                    temperature=0.2,
                    system_prompt="你是一个专业的程序员。请生成高质量、可运行的代码，包含适当的注释和错误处理。代码应该遵循最佳实践。"
                )
                end_time = time.time()
                
                if response['success']:
                    print(f"\n✅ 代码生成完成! (用时: {end_time - start_time:.2f}s)")
                    print("=" * 50)
                    print(response['content'])
                    print("=" * 50)
                    
                    if response.get('usage'):
                        usage = response['usage']
                        print(f"\n📊 使用情况: {usage.get('total_tokens', 'N/A')} tokens")
                else:
                    print(f"❌ 生成失败: {response['error']}")
                
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                
            print("\n" + "-" * 60 + "\n")
    
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")

if __name__ == "__main__":
    # 只运行Vue.js登录表单测试
    test_code_generation()