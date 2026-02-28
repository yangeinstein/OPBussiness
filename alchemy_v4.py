import requests
import json
from datetime import datetime

# 1. 暴力提取密码
notion_secret = None
deepseek_key = None
with open('.env', 'r', encoding='utf-8-sig') as f:
    for line in f:
        if 'NOTION_API_KEY' in line: notion_secret = line.split('=', 1)[1].strip()
        if 'DEEPSEEK_API_KEY' in line: deepseek_key = line.split('=', 1)[1].strip()

DATABASE_ID = "60e9a7f"
NOTION_HEADERS = {
    "Authorization": f"Bearer {notion_secret}",
    "Notion-Version": "2022-06-28", 
    "Content-Type": "application/json"
}

def fetch_latest():
    print("📡 正在从 Notion 档案柜调取最新灵感...")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "page_size": 1,
        "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}]
    }
    res = requests.post(url, headers=NOTION_HEADERS, json=payload)
    data = res.json().get("results", [])
    
    if not data: return None, None
    page_id = data[0]["id"]
    props = data[0].get("properties", {})
    title_list = props.get("Name", {}).get("title", [])
    raw_text = title_list[0]['plain_text'] if title_list else None
    return raw_text, page_id

def young_sir_alchemy(text):
    now_display = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🧬 Young Sir 分身接入算力中心 | 时间坐标: {now_display}")
    
    system_prompt = """
    你是一个名为 Young Sir 的数字分身。INTJ 战略型，一人公司架构师。
    【公众号排版规范 - 绝密执行】：
    1. 必须使用标准中文全角标点（，。？！）。严禁省略标点。
    2. 每一段话不得超过 2 行，段落之间必须使用 两个回车 进行强制换行。
    3. 严禁使用 **、### 等 Markdown 符号。
    4. 风格：冷峻、碎裂，但字里行间要有深夜备忘录的真实温热感。
    """
    
    user_prompt = f"""
    当前时间：{now_display}
    原始灵感：'{text}'
    
    请按以下思维模型生成：
    【看到】：描述具体的视觉或生活碎片。
    【想到】：跳跃到商业逻辑、拆解或长尾效应的深度思考。
    【联想】：链接到主导宿命、一人公司的知识库护城河。
    【生成】：一份直接发公众号的备忘录。
    
    结尾固定句式：我是 Young Sir，干就完了。
    """
    
    headers = {"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        "temperature": 0.8
    }
    res = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=data)
    content = res.json()['choices'][0]['message']['content']
    
    # 注入时间戳标题
    return f"【Young Sir 战略日志 | {now_display}】\n\n{content}"

def update_notion(page_id, content):
    print("🧪 炼金完成，正在精准回写至 [公众号文章] 列...")
    iso_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+08:00")
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "公众号文章": {"rich_text": [{"text": {"content": content}}]},
            "Date": {"date": {"start": iso_time}}
        }
    }
    response = requests.patch(url, headers=NOTION_HEADERS, json=payload)
    return response.status_code == 200

if __name__ == "__main__":
    raw, pid = fetch_latest()
    if raw:
        final_result = young_sir_alchemy(raw)
        if update_notion(pid, final_result):
            print("\n" + "="*50)
            print("✅ 满分操作！带标点、带换行的成品已同步回 Notion。")
            print("="*50)
            print(f"\n预览：\n{final_result[:200]}...")