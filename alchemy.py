import requests
import json

# 1. 暴力强拆保险箱 (读取 .env)
notion_secret = None
deepseek_key = None
with open('.env', 'r', encoding='utf-8-sig') as f:
    for line in f:
        if 'NOTION_API_KEY' in line:
            notion_secret = line.split('=', 1)[1].strip()
        if 'DEEPSEEK_API_KEY' in line:
            deepseek_key = line.split('=', 1)[1].strip()

# 2. 配置中心
DATABASE_ID = "313b5480ec7580fda82bdbb8160e9a7f" # 已验证的 ID
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

# --- 第一阶段：从 Notion 抓取灵感 ---
def get_latest_idea():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {notion_secret}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    # 仅获取最新的一条记录
    payload = {"page_size": 1}
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        if not results:
            return None
        # 提取标题内容
        props = results[0].get("properties", {})
        title_obj = props.get("Name", props.get("标题", {}))
        title_list = title_obj.get("title", [])
        return title_list[0]['plain_text'] if title_list else None
    return None

# --- 第二阶段：调用 DeepSeek 炼金 ---
def alchemize(raw_text):
    print(f"🧬 正在炼制灵感: {raw_text}")
    
    # 注入 Dan Koe 风格的 Prompt
    system_prompt = """
    你是一个擅长 Dan Koe 风格的内容创作者。你的目标是将琐碎的日记碎片转化为具有哲学深度的社交媒体文案。
    风格指南：
    1. 使用对立统一（Antithesis）：如“混乱中的秩序”、“痛苦中的自由”。
    2. 关注个人主权、数字资产、心理认知和现代生产力。
    3. 结构：吸引人的Hook + 逻辑拆解 + 极简的总结。
    4. 语气：冷静、深刻、具有煽动性。
    """
    
    user_prompt = f"请将这段灵感碎片扩写为一段 Dan Koe 风格的推文：'{raw_text}'"
    
    headers = {
        "Authorization": f"Bearer {deepseek_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }
    
    response = requests.post(DEEPSEEK_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ 炼金失败，API 错误: {response.text}"

# --- 主程序运行 ---
if __name__ == "__main__":
    print("🔮 贾维斯正在启动炼金炉...")
    idea = get_latest_idea()
    
    if idea:
        result = alchemize(idea)
        print("\n" + "="*50)
        print("✨ 炼金成品：")
        print("="*50)
        print(result)
        print("="*50)
    else:
        print("📭 档案柜里空空如也，请先在 Notion 里录入灵感。")