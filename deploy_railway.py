#!/usr/bin/env python3
"""Deploy DomainSentry to Railway using Playwright browser automation"""

from playwright.sync_api import sync_playwright
import subprocess, time, sys

RAILWAY_EMAIL = "ibyos@resend.dev"  # Will be created
RAILWAY_PASS = "IbyosRailway2026!"

GITHUB_REPO = "https://github.com/ibyos/cipherwatch"

def run_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True, args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = ctx.new_page()
    page.set_default_timeout(30000)
    return p, browser, ctx, page

def wait_for_load(page, selector, timeout=15000):
    try:
        page.wait_for_selector(selector, timeout=timeout)
        return True
    except:
        return False

print("Starting Railway deployment via browser automation...")

p, browser, ctx, page = run_browser()

try:
    # Step 1: Go to Railway
    print("[1/6] Opening Railway...")
    page.goto("https://railway.app", wait_until="domcontentloaded")
    time.sleep(2)
    
    # Check if already logged in
    if page.url == "https://railway.app/dashboard" or "dashboard" in page.url:
        print("Already logged in to Railway!")
    else:
        # Click Sign Up
        print("[2/6] Looking for sign up...")
        page.screenshot(path="/tmp/railway_1.png")
        
        # Try to find signup button
        signup_clicked = False
        for selector in [
            'text="Sign up"',
            'text="Get Started"',
            'text="Sign Up Free"',
            'a[href*="signup"]',
            'a[href*="register"]',
        ]:
            try:
                page.click(selector, timeout=3000)
                signup_clicked = True
                print(f"Clicked: {selector}")
                break
            except:
                pass
        
        if not signup_clicked:
            page.goto("https://railway.app/signup")
            time.sleep(3)
        
        page.screenshot(path="/tmp/railway_2.png")
        print(f"Current URL: {page.url}")
        print("Manual screenshot saved to /tmp/railway_*.png")
        print("Please check screenshots and provide the Railway API token instead.")
        print("Go to railway.app -> Settings -> API Tokens -> Create token")
        browser.close()
        p.stop()
        sys.exit(1)

finally:
    browser.close()
    p.stop()
