#!/usr/bin/env python3
"""DomainSentryBot — Public brand protection scanner for everyone"""

import urllib.request, urllib.parse, json, time, socket
from datetime import datetime

BOT_TOKEN = "8811012185:AAFiM-TROUOA0I26ppoArRXF1hflHk9PU0A"  # Will be set by CJ
ADMINS = ["8321638328"]  # CJ is admin

TLDs = ['ru', 'com', 'net', 'org', 'biz', 'info', 'su']
SIMILAR = {
    'a': ['e','4'], 'b': ['d'], 'c': ['e','k'],
    'e': ['3'], 'i': ['1','l'], 'o': ['0'],
    's': ['5'], 't': ['7'], 'u': ['v'],
    'w': ['vv'], '0': ['o'], '1': ['i'],
}

def extract_base(t):
    t = t.replace('https://','').replace('http://','').split('/')[0]
    return t.replace('www.','')

def generate(base):
    v = {base}
    for i, c in enumerate(base):
        for s in SIMILAR.get(c.lower(), []):
            v.add(base[:i] + s + base[i+1:])
    for i in range(1, len(base)):
        v.add(base[:i] + '-' + base[i:])
    return sorted(v)

def check(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return None

def send(chat_id, text, reply=False):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
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

def handle(chat_id, text):
    text = text.strip()
    
    if text in ['/start', '/help']:
        send(chat_id, "🔒 <b>DomainSentry Bot</b>\n\nFind typosquatting & brand impersonation domains.\n\nCommands:\n/scan &lt;domain&gt; — scan brand\n/pricing — view plans\n/about — about us")
    
    elif text.startswith('/scan '):
        domain = text.split('/scan ', 1)[1].strip().replace('https://','').replace('http://','')
        send(chat_id, f"🔍 Scanning <code>{domain}</code>...\n⏳ This takes 20-40 seconds...")
        base = extract_base(domain)
        variants = generate(base)
        threats = []
        for v in variants:
            for tld in TLDs:
                d = f"{v}.{tld}"
                ip = check(d)
                if ip:
                    threats.append(f"  ⚠️ <code>{d}</code> → {ip}")
        
        if threats:
            msg = f"⚠️ <b>{len(threats)} threats found</b> for {base}:\n\n" + "\n".join(threats[:15])
            if len(threats) > 15:
                msg += f"\n...and {len(threats)-15} more."
        else:
            msg = f"✅ <b>Clean!</b>\nNo typosquatting variants registered for {base}.\nChecked {len(variants)*len(TLDs)} domain combinations."
        
        send(chat_id, msg)
    
    elif text == '/pricing':
        send(chat_id, "💰 <b>Pricing</b>\n\nFree — $0/mo\n• 1 domain\n• Daily scan\n\nPro — $9.99/mo\n• 10 domains\n• Real-time alerts\n• API access\n\nBusiness — $29.99/mo\n• 50 domains\n• Webhook alerts\n• Priority support\n\n/start to subscribe")
    
    elif text == '/about':
        send(chat_id, "🏢 <b>DomainSentry</b>\n\nBrand protection SaaS — find typosquatting, copycats and lookalike domains.\n\nBuilt by ⚡ ibyos")
    
    else:
        send(chat_id, "Use /scan &lt;domain&gt; to check a domain.\nOr /help for all commands.")

LAST_UPDATE = 0

def main():
    global LAST_UPDATE, BOT_TOKEN
    print("DomainSentryBot ready — public access")
    print(f"Admins: {ADMINS}")
    
    if BOT_TOKEN == "TO BE SET":
        print("ERROR: Set BOT_TOKEN in the script first!")
        return
    
    while True:
        try:
            updates = get_updates(LAST_UPDATE + 1)
            for upd in updates.get("result", []):
                LAST_UPDATE = upd["update_id"]
                msg = upd.get("message", {})
                chat_id = str(msg.get("chat", {}).get("id", ""))
                text = msg.get("text", "")
                if text:
                    print(f"[{chat_id}] {text[:50]}")
                    handle(chat_id, text)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
