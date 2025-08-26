# AI模型对接Demo

这是一个Python项目，用于对接和测试多个主流AI模型平台的API接口。

## 支持的平台

- **OpenAI** - GPT系列模型
- **通义千问 (Qwen)** - 阿里云大模型
- **智谱AI (ZhipuAI)** - GLM系列模型  
- **百度千帆 (Baidu Qianfan)** - 文心一言等模型
- **AIHubMix** - 第三方AI聚合平台

## 项目结构

```
ai-model-demo/
├── config/
│   └── config.py          # 配置文件
├── platforms/             # 各平台客户端实现
│   ├── openai/           # OpenAI客户端
│   │   ├── __init__.py
│   │   └── client.py
│   ├── qwen/             # 通义千问客户端
│   │   ├── __init__.py
│   │   └── client.py
│   ├── zhipu/            # 智谱AI客户端
│   │   ├── __init__.py
│   │   └── client.py
│   ├── baidu/            # 百度千帆客户端
│   │   ├── __init__.py
│   │   └── client.py
│   ├── aihubmix/         # AIHubMix客户端
│   │   ├── __init__.py
│   │   └── client.py
│   └── __init__.py       # 统一管理器
├── tests/                # 测试和查询脚本
│   ├── test_all_platforms.py      # 所有平台测试
│   ├── test_single_platform.py    # 单平台测试
│   ├── test_code_generation.py    # 代码生成专项测试
│   ├── get_qwen_models.py         # 通义千问模型查询
│   ├── get_openai_models.py       # OpenAI模型查询
│   ├── get_zhipu_models.py        # 智谱AI模型查询
│   ├── get_baidu_models.py        # 百度千帆模型查询
│   └── get_aihubmix_models.py     # AIHubMix模型查询
├── main.py              # 主程序入口
├── pyproject.toml       # uv项目配置
├── uv.lock             # 依赖锁定文件
└── README.md           # 项目说明
```

## 安装和配置

### 1. 环境准备

确保安装了Python 3.8+和uv包管理工具。

### 2. 安装依赖

```bash
# 项目已使用uv初始化，依赖会自动安装
uv sync
```

### 3. 配置API密钥

创建`.env`文件并配置你的API密钥：

```bash
# 创建环境变量文件
touch .env
```

编辑`.env`文件，填入你的API密钥：

```env
# OpenAI配置
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1

# 通义千问配置 (阿里云DashScope)
# 注意：通义千问不需要配置URL，SDK内置端点: https://dashscope.aliyuncs.com/api/v1
# 获取API Key: https://dashscope.console.aliyun.com/
QWEN_API_KEY=your_qwen_api_key

# 智谱AI配置
# 注意：智谱AI也不需要配置API URL，SDK内置了端点
ZHIPU_API_KEY=your_zhipu_api_key

# 百度千帆配置
# 注意：百度千帆也不需要配置API URL，SDK内置了端点
# 需要API Key和Secret Key两个密钥
BAIDU_API_KEY=your_baidu_api_key
BAIDU_SECRET_KEY=your_baidu_secret_key

# AIHubMix配置 (第三方平台)
# 注意：第三方平台需要配置API URL，因为端点不固定
AIHUBMIX_API_KEY=your_aihubmix_api_key
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
```

## 使用方法

### 1. 运行主程序

```bash
python main.py
```

这会显示支持的平台并运行简单测试。

### 2. 测试所有平台

```bash
python tests/test_all_platforms.py
```

这会自动测试所有已配置API密钥的平台。

### 3. 测试单个平台

```bash
# 普通模式测试
python tests/test_single_platform.py openai -m "你好"

# 流式输出测试
python tests/test_single_platform.py qwen -m "介绍一下Python" -s
python tests/test_single_platform.py qwen -m "使用vue写一个简单的登录页面" -s

# 交互模式
python tests/test_single_platform.py zhipu -i
```

支持的平台参数：`qwen`, `openai`, `zhipu`, `baidu`, `aihubmix`

### 4. 代码生成测试

专门测试AI模型的代码生成能力：

```bash
# AIHubMix代码生成测试 (Vue.js登录表单)
python tests/test_code_generation.py
```

**测试内容：**
- 🎯 Vue.js登录表单生成
- 📊 详细性能统计
- 🔍 代码质量分析
- 🤖 支持多种模型切换

**支持的模型：**
- `gpt-4o` - OpenAI最新模型（默认）
- `gpt-5` - GPT-5模型（需要特殊配置）
- `gpt-4-turbo` - GPT-4 Turbo
- `claude-3-sonnet` - Claude 3 Sonnet

**修改测试模型：**
编辑 `tests/test_code_generation.py` 第65行：
```python
model_to_use = "gpt-5"  # 改为你想测试的模型
```

### 5. 查询平台支持的模型列表

#### 各平台模型列表查询脚本

```bash
# 通义千问模型查询
python tests/get_qwen_models.py

# OpenAI模型查询
python tests/get_openai_models.py

# 智谱AI模型查询  
python tests/get_zhipu_models.py

# 百度千帆模型查询
python tests/get_baidu_models.py

# AIHubMix模型查询
python tests/get_aihubmix_models.py
```

### 6. 编程使用

```python
from platforms import AIModelManager

# 创建管理器
manager = AIModelManager()

# 普通聊天
response = manager.chat('openai', '你好，世界！')
if response['success']:
    print(response['content'])

# 流式聊天
for chunk in manager.chat_stream('qwen', '写一首诗'):
    if chunk['success']:
        print(chunk['content'], end='')
```

## API接口说明

### 统一接口

所有平台客户端都实现了相同的接口：

#### `chat(message, model=None, temperature=0.7, max_tokens=1000, **kwargs)`

发送聊天消息并获取回复。

**参数:**
- `message` (str): 用户消息
- `model` (str, 可选): 模型名称，默认使用配置中的模型
- `temperature` (float): 温度参数，控制回复的创造性
- `max_tokens` (int): 最大token数量
- `**kwargs`: 其他平台特定参数

**返回:**
```python
{
    'success': bool,      # 是否成功
    'content': str,       # 回复内容 (成功时)
    'error': str,         # 错误信息 (失败时)
    'model': str,         # 使用的模型
    'usage': dict         # token使用情况 (如果可用)
}
```

#### `chat_stream(message, **kwargs)`

流式聊天，逐步返回回复内容。

**返回:** 生成器，每次yield一个包含部分回复的字典。

### 平台特定配置

每个平台的特点和配置要求：

- **OpenAI**: 
  - 支持`system_prompt`参数
  - 可配置自定义`base_url`（支持代理服务）
  - 需要API Key
  - 默认模型：`gpt-4o`

- **通义千问**: 
  - 使用阿里云DashScope API
  - API端点内置在SDK中：`https://dashscope.aliyuncs.com/api/v1`
  - 只需要API Key，无需配置URL
  - 默认模型：`qwen-turbo`

- **智谱AI**: 
  - 支持GLM系列模型
  - API端点内置在SDK中
  - 只需要API Key，无需配置URL
  - 默认模型：`glm-4`

- **百度千帆**: 
  - 支持文心一言等百度模型
  - 需要API Key和Secret Key两个密钥
  - API端点内置在SDK中
  - 默认模型：`ernie-bot-turbo`

- **AIHubMix**: 
  - 兼容OpenAI API格式
  - 第三方聚合平台，需要配置`base_url`
  - 通常支持多种主流模型
  - 默认模型：`gpt-4o`
  - **智能参数支持**：自动检测模型类型，对GPT-5等新模型使用`max_completion_tokens`参数

### Token参数说明

**`max_tokens` 参数作用：**
- 🎯 **控制回复长度**：限制AI生成内容的最大token数量
- 💰 **节省费用**：多数AI服务按token计费
- ⚡ **控制响应时间**：更少token = 更快响应
- 📏 **Token换算**：1个token ≈ 0.75个英文单词 或 2-3个中文字符

**不同场景建议值：**
- **简单问答**：50-100 tokens
- **对话聊天**：200-500 tokens
- **代码生成**：500-2000 tokens
- **文章创作**：1000-4000 tokens

**模型兼容性：**
- **传统模型**（GPT-4, GPT-3.5等）：使用`max_tokens`参数
- **新模型**（GPT-5, o1等）：使用`max_completion_tokens`参数
- **本项目**：AIHubMix客户端会自动检测模型类型并使用正确参数

## 故障排除

### 1. API密钥未配置

```
❌ 没有找到任何配置的API密钥
```

**解决方法:** 
- 创建`.env`文件：`touch .env`
- 在`.env`文件中配置正确的API密钥（参考上面的配置示例）

### 2. 导入错误

```
ModuleNotFoundError: No module named 'platforms'
```

**解决方法:** 确保在项目根目录运行脚本，或正确设置Python路径。

### 3. API调用失败

检查：
- API密钥是否正确
- 网络连接是否正常  
- API配额是否充足
- 基础URL是否正确（对于第三方平台）
