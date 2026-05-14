#!/usr/bin/env python3
"""DomainSentry — FastAPI Backend"""

import os
import socket
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="DomainSentry")

SIMILAR = {
    'a': ['e','4'], 'b': ['d'], 'c': ['e','k'],
    'e': ['3'], 'i': ['1','l'], 'o': ['0'],
    's': ['5'], 't': ['7'], 'u': ['v'],
    'w': ['vv'], '0': ['o'], '1': ['i'],
}
TLDs = ['ru', 'com', 'net', 'org', 'biz', 'info', 'su']

def extract_base(target):
    target = target.replace('https://','').replace('http://','').split('/')[0]
    return target.replace('www.','')

def generate(base):
    variants = {base}
    for i, c in enumerate(base):
        for s in SIMILAR.get(c.lower(), []):
            variants.add(base[:i] + s + base[i+1:])
    for i in range(1, len(base)):
        variants.add(base[:i] + '-' + base[i:])
    return sorted(variants)

def check(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {'domain': domain, 'up': True, 'ip': ip}
    except:
        return {'domain': domain, 'up': False}

HTML = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DomainSentry — Brand Protection Scanner</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
.container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
.hero { text-align: center; margin-bottom: 50px; }
.logo { font-size: 2.5em; font-weight: 800; color: #00ff88; margin-bottom: 10px; }
.logo span { color: #ff6b35; }
.tagline { color: #888; font-size: 1.1em; margin-bottom: 40px; }
.search-box { display: flex; gap: 10px; justify-content: center; margin-bottom: 40px; flex-wrap: wrap; }
input { padding: 15px 20px; font-size: 1.1em; border: 2px solid #1a1a2e; border-radius: 12px; background: #12121a; color: #fff; width: 300px; outline: none; transition: border 0.3s; }
input:focus { border-color: #00ff88; }
button { padding: 15px 30px; font-size: 1.1em; background: linear-gradient(135deg, #00ff88, #00cc6a); color: #0a0a0f; font-weight: 700; border: none; border-radius: 12px; cursor: pointer; transition: transform 0.2s; }
button:hover { transform: scale(1.05); }
.status { text-align: center; padding: 20px; color: #888; font-size: 0.9em; }
.threat-card { background: #12121a; border: 1px solid #1a1a2e; border-radius: 16px; padding: 20px; margin-bottom: 15px; transition: border-color 0.3s; }
.threat-card:hover { border-color: #ff6b35; }
.threat-domain { font-size: 1.2em; font-weight: 700; color: #ff6b35; margin-bottom: 5px; }
.threat-ip { color: #666; font-family: monospace; font-size: 0.9em; }
.threat-badge { display: inline-block; background: #ff6b35; color: #0a0a0f; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: 700; margin-top: 8px; }
.summary { background: #12121a; border-radius: 16px; padding: 30px; text-align: center; margin-bottom: 30px; }
.summary h2 { color: #00ff88; font-size: 3em; margin-bottom: 5px; }
.summary p { color: #888; }
.pricing { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 60px; }
.plan { background: #12121a; border: 1px solid #1a1a2e; border-radius: 16px; padding: 30px; text-align: center; transition: border-color 0.3s; }
.plan:hover { border-color: #00ff88; }
.plan h3 { color: #fff; font-size: 1.3em; margin-bottom: 10px; }
.plan .price { font-size: 2.5em; font-weight: 800; color: #00ff88; }
.plan .price span { font-size: 0.4em; color: #666; }
.plan ul { list-style: none; margin-top: 20px; color: #888; }
.plan li { padding: 8px 0; }
.plan li::before { content: '✓ '; color: #00ff88; }
.footer { text-align: center; margin-top: 60px; color: #444; font-size: 0.85em; }
</style></head><body>
<div class="container">
<div class="hero"><div class="logo">Domain<span>Sentry</span></div>
<p class="tagline">Find typosquatting, brand infringement & malicious domains</p></div>
<div class="search-box">
<input type="text" id="domainInput" placeholder="yourbrand.com" value="apple" />
<button onclick="runScan()">Scan</button>
</div>
<div class="status" id="status">Ready. Enter a domain and hit Scan.</div>
<div id="summary" style="display:none;"></div>
<div id="results" class="results"></div>
<div class="pricing">
<div class="plan"><h3>Free</h3><div class="price">$0<span>/mo</span></div><ul><li>1 domain</li><li>Daily scan</li><li>Email alerts</li></ul></div>
<div class="plan" style="border-color:#00ff88;"><h3>Pro ⭐</h3><div class="price">$9<span>.99/mo</span></div><ul><li>10 domains</li><li>Real-time alerts</li><li>API access</li></ul></div>
<div class="plan"><h3>Business</h3><div class="price">$29<span>.99/mo</span></div><ul><li>50 domains</li><li>Webhook alerts</li><li>Priority support</li></ul></div>
</div>
<div class="footer">DomainSentry v0.1-alpha — Built by ibyos ⚡</div>
</div>
<script>
async function runScan() {
    const domain = document.getElementById('domainInput').value.trim();
    if (!domain) return;
    const status = document.getElementById('status');
    const results = document.getElementById('results');
    const summary = document.getElementById('summary');
    status.textContent = `Scanning ${domain}...`;
    results.innerHTML = '';
    summary.style.display = 'none';
    try {
        const resp = await fetch('/scan', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: `domain=${encodeURIComponent(domain)}` });
        const data = await resp.json();
        if (data.count === 0) {
            summary.innerHTML = `<div class="summary"><h2>✅ 0</h2><p>No typosquatting variants registered for <strong>${data.target}</strong><br>Checked ${data.checked} domain combinations.</p></div>`;
        } else {
            let cards = data.threats.map(t => `<div class="threat-card"><div class="threat-domain">${t.domain}</div><div class="threat-ip">IP: ${t.ip || 'unknown'}</div><span class="threat-badge">⚠️ REGISTERED</span></div>`).join('');
            summary.innerHTML = `<div class="summary"><h2>${data.count}</h2><p>Active threats found for <strong>${data.target}</strong><br>Checked ${data.checked} domain combinations.</p></div>`;
            results.innerHTML = cards;
        }
        status.textContent = 'Scan complete.';
        summary.style.display = 'block';
    } catch(e) { status.textContent = 'Error: ' + e.message; }
}
document.getElementById('domainInput').addEventListener('keydown', e => { if (e.key === 'Enter') runScan(); });
</script></body></html>'''

@app.get("/")
def index():
    return HTMLResponse(content=HTML)

@app.post("/scan")
def scan(domain: str = Form(...)):
    base = extract_base(domain)
    variants = generate(base)
    results = []
    checked = 0
    for v in variants:
        for tld in TLDs:
            d = f"{v}.{tld}"
            checked += 1
            r = check(d)
            if r['up']:
                results.append(r)
    return {
        'target': base,
        'checked': checked,
        'threats': results,
        'count': len(results)
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
