import time
import requests
import os
from threading import Thread
from flask import Flask

TOKEN = "9218505324:AAH5dFo4fhmKYwRkY1ngmCUTIfquv8cbE"
CHAT_ID = "5340646272"
FILE_UID = "uids.txt"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Loi: {e}")

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except:
        return None

def load_uids():
    try:
        if not os.path.exists(FILE_UID):
            return []
        with open(FILE_UID, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return [line.strip() for line in lines if line.strip()]
    except:
        return []

def save_uid(uid):
    uids = load_uids()
    if uid not in uids:
        with open(FILE_UID, "a", encoding="utf-8") as f:
            f.write(uid + "\n")
        return True
    return False

def check_facebook_uid(uid):
    url = f"https://graph.facebook.com/{uid}/picture?type=normal"
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.status_code == 404:
            return "DIE"
        final_url = response.url
        if "scontent" in final_url or "fbcdn.net" in final_url:
            return "LIVE"
        else:
            return "CHECKPOINT/DIE"
    except:
        return "UNKNOWN"

def run_bot():
    print("Bot quan ly UID qua Telegram dang chay tren Cloud...")
    send_telegram_message("🤖 *Bot đã lên mây thành công!*\n- Sẵn sàng nhận UID trực tiếp 24/7.")
    
    last_update_id = 0
    last_check_time = 0

    while True:
        try:
            updates = get_updates(offset=last_update_id + 1)
            if updates and "result" in updates:
                for update in updates["result"]:
                    last_update_id = update["update_id"]
                    if "message" in update and "text" in update["message"]:
                        text = update["message"]["text"].strip()
                        
                        if text.startswith("/list"):
                            uids = load_uids()
                            send_telegram_message(f"📋 *Danh sách UID đang theo dõi:*\n" + "\n".join(uids) if uids else "Chưa có UID nào.")
                        elif text.isdigit():
                            if save_uid(text):
                                send_telegram_message(f"✅ *Đã thêm thành công UID:* `{text}`")
                            else:
                                send_telegram_message(f"⚠️ UID `{text}` đã tồn tại trong danh sách từ trước.")

            current_time = time.time()
            if current_time - last_check_time > 300:
                uids = load_uids()
                if uids:
                    for uid in uids:
                        current_status = check_facebook_uid(uid)
                last_check_time = current_time
        except Exception as e:
            print(f"Loop error: {e}")

        time.sleep(2)

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    run_bot()