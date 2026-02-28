import requests

# 1. 暴力提取密码
notion_secret = None
with open('.env', 'r', encoding='utf-8-sig') as f:
    for line in f:
        if 'NOTION_API_KEY' in line:
            notion_secret = line.split('=', 1)[1].strip()

# 2. 修正后的 32 位 Database ID (严禁删改长度)
database_id = "0e9a7f" 

url = f"https://api.notion.com/v1/databases/{database_id}/query"
headers = {
    "Authorization": f"Bearer {notion_secret}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

try:
    print("贾维斯正在执行 P0 任务：最后的连接尝试...")
    response = requests.post(url, headers=headers, json={})
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        print("==================================================")
        print(f"✅ 战报：连接彻底打通！已读取 {len(results)} 条数据。")
        for page in results:
            # 自动适配：尝试读取名为 'Name' 或 '标题' 的列
            props = page.get("properties", {})
            title_obj = props.get("Name", props.get("标题", {}))
            title_list = title_obj.get("title", [])
            if title_list:
                print(f"📌 内容: {title_list[0]['plain_text']}")
        print("==================================================")
    else:
        print(f"❌ 失败。保安代码：{response.status_code}")
        print(f"❌ 保安原话：{response.text}")
        print("请检查：Notion 页面右上角 ... -> Connect to 里面是否选了 Jarvis_Brain")
except Exception as e:
    print(f"❌ 程序奔溃: {e}")