#!/usr/bin/env python3
"""ibyos Status Reporter — sends Telegram updates every minute"""

import urllib.request, urllib.parse, time, os, subprocess
from datetime import datetime

BOT = "8620446057:AAEMe7umuNp73O8PK26bbI4sZtlWgTlYglg"
CHAT = "8321638328"

def send(text):
    url = f"https://api.telegram.org/bot{BOT}/sendMessage"
    data = f"chat_id={CHAT}&text={urllib.parse.quote(text)}&parse_mode=HTML"
    req = urllib.request.Request(url, data.encode(), {"Content-Type": "application/x-www-form-urlencoded"})
    try:
        urllib.request.urlopen(req, timeout=10)
        print(f"[{datetime.now().strftime('%H:%M')}] Sent: {text[:60]}")
    except Exception as e:
        print(f"Error: {e}")

build_status = {
    "scanner": "✅ Advanced scanner v0.2 ready",
    "api": "✅ FastAPI + Web UI on port 5000",
    "telegram": "✅ Telegram bot connected",
    "whois": "✅ Whois + age detection integrated",
    "roadmap": "✅ Marketing strategy documented",
    "next": "⏳ CI/CD pipeline",
    "next2": "⏳ Email alerts (SMTP)",
    "next3": "⏳ User auth system",
    "next4": "⏳ Dashboard + PDF reports",
}

def build_report():
    lines = [
        "⚡ <b>ibyos Status Update</b>",
        f"🕐 {datetime.now().strftime('%H:%M:%S')}",
        "",
        "<b>Completed:</b>",
    ]
    for k, v in build_status.items():
        if v.startswith("✅"):
            lines.append(f"  {v}")
    
    lines += ["", "<b>In progress:</b>"]
    for k, v in build_status.items():
        if v.startswith("⏳"):
            lines.append(f"  {v}")
    
    return "\n".join(lines)

send(build_report())

# Continue every 60 seconds
import atexit
atexit.register(lambda: send("🔴 ibyos going offline"))

print("Status reporter running. Press Ctrl+C to stop.")
while True:
    time.sleep(60)
    send(build_report())
