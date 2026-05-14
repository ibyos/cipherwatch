#!/usr/bin/env python3
"""Telegram Status Reporter for DomainSentry Build"""

import subprocess, json
from datetime import datetime

BOT_TOKEN = "8620446057:AAEMe7umuNp73O8PK26bbI4sZtlWgTlYglg"
CHAT_ID = "8321638328"

def send(text):
    import urllib.request
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = f"chat_id={CHAT_ID}&text={urllib.parse.quote(text)}&parse_mode=HTML"
    req = urllib.request.Request(url, data.encode(), {"Content-Type": "application/x-www-form-urlencoded"})
    urllib.request.urlopen(req, timeout=10)

send("⚡ <b>DomainSentry</b> build session\n📅 06:14 UTC\n\n✅ Scanner v0.2 (Whois + age detection)\n✅ API + Web UI\n⏳ Telegram alerts + CI/CD\n\nStarted building...")
