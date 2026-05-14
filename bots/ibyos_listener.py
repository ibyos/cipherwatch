#!/usr/bin/env python3
"""ibyosBot — Personal assistant, CJ only"""

import urllib.request, urllib.parse, json, time, os, sys

BOT_TOKEN = "8620446057:AAEMe7umuNp73O8PK26bbI4sZtlWgTlYglg"
ALLOWED_CHAT_ID = "8321638328"
LAST_UPDATE = 0

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def send(chat_id, text, reply_to=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_to:
        data["reply_to_message_id"] = reply_to
    req = urllib.request.Request(url, json.dumps(data).encode(), {"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"Send error: {e}")

def get_updates(offset=0):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req, timeout=35)
        return json.loads(resp.read())
    except:
        return {}

def handle_command(chat_id, text, msg_id):
    text = text.strip()
    
    if text.startswith('/start') or text.startswith('/help'):
        send(chat_id, "⚡ ibyos personal assistant\n\nCommands:\n/scan <domain> — scan domains\n/status — build status\n/projects — list projects\n/uptime — uptime info")
    
    elif text.startswith('/scan '):
        domain = text.split('/scan ', 1)[1].strip()
        send(chat_id, f"🔍 Scanning <code>{domain}</code>...")
        import subprocess
        result = subprocess.run(
            ["python3", f"{BASE_DIR}/app/scanner.py", domain],
            capture_output=True, text=True, timeout=60
        )
        output = result.stdout + result.stderr
        lines = [l for l in output.split('\n') if l.strip()][:10]
        send(chat_id, "📊 Result:\n\n" + "\n".join(lines[:8]))
    
    elif text.startswith('/status'):
        send(chat_id, "⚡ <b>DomainSentry Build</b>\n\n✅ Advanced scanner v0.2\n✅ API + Web UI\n✅ Whois + age detection\n✅ Telegram bot (this)\n⏳ CI/CD pipeline\n⏳ Email alerts\n⏳ User auth")
    
    elif text.startswith('/projects'):
        send(chat_id, "📁 Projects:\n\n• DomainSentry — Brand Protection SaaS\n• Location: /home/kalikali/projects/cipherwatch")
    
    elif text.startswith('/uptime'):
        import subprocess
        r = subprocess.run(["uptime"], capture_output=True, text=True)
        send(chat_id, f"🖥️ {r.stdout.strip()}")
    
    else:
        send(chat_id, "⚡ Я ibyos. Команди:\n/scan <domain>\n/status\n/projects\n/uptime", reply_to=msg_id)

def main():
    global LAST_UPDATE
    print("ibyosBot running — CJ only mode")
    print(f"Allowed chat_id: {ALLOWED_CHAT_ID}")
    
    while True:
        try:
            updates = get_updates(LAST_UPDATE + 1)
            for upd in updates.get("result", []):
                LAST_UPDATE = upd["update_id"]
                msg = upd.get("message", {})
                chat_id = str(msg.get("chat", {}).get("id", ""))
                text = msg.get("text", "")
                msg_id = msg.get("message_id")
                
                if chat_id == ALLOWED_CHAT_ID:
                    print(f"[CJ] {text[:60]}")
                    handle_command(chat_id, text, msg_id)
                else:
                    print(f"[BLOCKED] chat_id={chat_id} — not CJ")
                    send(chat_id, "⛔ Sorry, this bot is private.")
        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
