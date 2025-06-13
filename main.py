import time
import requests

API_URL = "https://script.google.com/macros/s/AKfycbxGToJVM3wucRsMjN8IQChSVoOseYcdbqLbGgXWpusPlsAYWqMXiudekP7jPYd-EoA/exec"  # ใส่ลิงก์ Web App
DISCORD_WEBHOOK = "https://ptb.discord.com/api/webhooks/1382831229681930300/gFhSSjfKBamc9hFGBJ7KEZOEcSpPjBmV3h8t_o5n6pGfCsIWeGFhIZbGYtF9IDlQcZOW"  # ใส่ลิงก์ Webhook

CHECK_INTERVAL = 30  # วินาที
sent_bosses = set()

def parse_hms_to_seconds(hms):
    try:
        h, m, s = map(int, hms.strip().split(":"))
        return h * 3600 + m * 60 + s
    except:
        return None

def check_and_notify():
    global sent_bosses
    response = requests.get(API_URL)
    if response.status_code != 200:
        print("❌ ดึงข้อมูลไม่สำเร็จ")
        return

    data = response.json()
    notify_list = []

    for entry in data:
        name = entry.get("boss")
        hms = entry.get("cooldown")

        seconds = parse_hms_to_seconds(hms)
        if seconds is None:
            continue

        if seconds <= 300:
            if name not in sent_bosses:
                notify_list.append(f"🔴 **{name}** จะเกิดในไม่เกิน {seconds // 60} นาที")
                sent_bosses.add(name)
        else:
            sent_bosses.discard(name)

    if notify_list:
        payload = {
            "content": "\n".join(notify_list)
        }
        res = requests.post(DISCORD_WEBHOOK, json=payload)
        print("✅ แจ้งเตือนแล้ว:", notify_list)

while True:
    try:
        check_and_notify()
    except Exception as e:
        print("⚠️ ERROR:", e)
    time.sleep(CHECK_INTERVAL)
