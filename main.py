import os
from dotenv import load_dotenv
from interpreter import interpreter

# 1. 打开保险箱，读取环境变量
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# 【防错机制】检查是否拿到了密码
if not api_key:
    print("❌ 报错啦：保险箱里没找到 API Key，请检查 .env 文件是否配置正确！")
    exit()

# 2. 接入 DeepSeek 大脑
interpreter.llm.api_key = api_key
interpreter.llm.model = "deepseek/deepseek-chat"
# 【补全遗漏点】明确指定 DeepSeek 的服务器大门，防止跑错去 OpenAI
interpreter.llm.api_base = "https://api.deepseek.com" 

# 3. 贯彻老板的安全红线：绝对审批锁 
interpreter.auto_run = False  

# 4. 唤醒贾维斯并开启对话
print("==================================================")
print("老板好，贾维斯引擎已启动，API保险箱已上锁，物理隔离开启。")
print("==================================================")

# 发送第一条测试指令
interpreter.chat("你好，贾维斯。请用一句简短的话向我做个自我介绍。")