#!/usr/bin/env python3
"""DomainSentry — Advanced Brand Protection Scanner v0.2"""

import socket
import whois
import json
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

TLDs = ['ru', 'com', 'net', 'org', 'biz', 'info', 'su', 'рф', 'com.ru', 'net.ru']

SIMILAR = {
    'a': ['e','4','@'], 'b': ['d','v','8'], 'c': ['e','k'],
    'e': ['3','€'], 'i': ['1','l','!'], 'l': ['1','|'],
    'o': ['0','ø'], 's': ['5','$','z'], 't': ['7','+'],
    'u': ['v','w'], 'v': ['u','w'], 'w': ['vv'],
    '0': ['o','O'], '1': ['i','l'], '5': ['s','$'],
}

def extract_base(target):
    target = target.replace('https://','').replace('http://','').split('/')[0]
    return target.replace('www.','')

def generate_variants(base):
    variants = {base}
    for i, c in enumerate(base):
        for s in SIMILAR.get(c.lower(), []):
            variants.add(base[:i] + s + base[i+1:])
            variants.add(s + base)
            variants.add(base + s)
    for i in range(1, len(base)):
        variants.add(base[:i] + '-' + base[i:])
    for i in range(2, len(base)-1):
        variants.add(base[:i] + '.' + base[i+1:])
    return sorted(variants)

def get_dns(domain):
    result = {'domain': domain, 'dns': {}}
    for qtype in ['A', 'AAAA', 'MX', 'NS']:
        try:
            import dns.resolver
            ans = dns.resolver.resolve(domain, qtype, timeout=2)
            result['dns'][qtype] = [str(rdata) for rdata in ans]
        except:
            pass
    return result

def get_whois(domain):
    result = {'whois': {}}
    try:
        w = whois.whois(domain)
        result['whois'] = {
            'registrar': w.registrar,
            'creation_date': str(w.creation_date)[:10] if w.creation_date else None,
            'expiration_date': str(w.expiration_date)[:10] if w.expiration_date else None,
            'name_servers': w.name_servers[:3] if w.name_servers else None,
            'emails': w.emails[:2] if w.emails else None,
        }
        if w.creation_date:
            age_days = (datetime.now() - w.creation_date.replace(tzinfo=None)).days
            result['whois']['age_days'] = age_days
    except Exception as e:
        result['whois']['error'] = str(e)[:50]
    return result

def check_domain(domain):
    result = {'domain': domain, 'registered': False, 'ip': None, 'whois': {}, 'dns': {}}
    try:
        ip = socket.gethostbyname(domain)
        result['registered'] = True
        result['ip'] = ip
        # Only do whois for registered domains
        try:
            w = whois.whois(domain)
            result['whois'] = {
                'registrar': str(w.registrar)[:60] if w.registrar else None,
                'created': str(w.creation_date)[:10] if w.creation_date else None,
                'ns': (w.name_servers or [None])[:2],
                'age_days': None
            }
            if w.creation_date:
                try:
                    cd = w.creation_date
                    if hasattr(cd, 'replace'):
                        result['whois']['age_days'] = (datetime.now() - cd.replace(tzinfo=None)).days
                except:
                    pass
        except:
            pass
    except:
        pass
    return result

def scan(target, max_workers=20, show_all=False):
    base = extract_base(target)
    variants = generate_variants(base)
    
    print(f"[+] Target: {base}")
    print(f"[+] Variants: {len(variants)} × {len(TLDs)} TLDs = {len(variants)*len(TLDs)} checks")
    
    threats, checked = [], 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {}
        for v in variants:
            for tld in TLDs:
                d = f"{v}.{tld}"
                checked += 1
                futures[ex.submit(check_domain, d)] = d
        
        for fut in as_completed(futures):
            r = fut.result()
            if r['registered']:
                age = r['whois'].get('age_days', 0)
                suspicious = age and age < 180  # younger than 6 months
                flag = "⚠️ SUSPICIOUS" if suspicious else "✅ Established"
                print(f"  {flag} | {r['domain']} | IP:{r['ip']} | Age:{age or '?'}d | Registrar:{r['whois'].get('registrar','?')}")
                threats.append(r)
    
    threats.sort(key=lambda x: (x['whois'].get('age_days', 99999) or 99999, x['domain']))
    
    report = {
        'target': base,
        'checked': checked,
        'threats_found': len(threats),
        'suspicious': [t for t in threats if t['whois'].get('age_days') and t['whois']['age_days'] < 180],
        'all_registered': threats,
    }
    return report

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('target')
    p.add_argument('--json', action='store_true')
    args = p.parse_args()
    
    result = scan(args.target)
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {result['threats_found']} registered domains found")
    print(f"SUSPICIOUS (<6mo): {len(result['suspicious'])}")
    print('='*60)
    
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print("\n--- Top Suspicious ---")
        for t in result['suspicious'][:5]:
            print(f"  {t['domain']} | Age: {t['whois'].get('age_days','?')}d | IP: {t['ip']} | {t['whois'].get('registrar','?')}")
