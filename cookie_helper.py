#!/usr/bin/env python3
"""
Helper script to create a cookies file for Instagram downloads
"""

import json
import sys
from pathlib import Path

def create_cookie_file():
    """Guide user through creating a cookie file"""
    print("Instagram Cookie Helper")
    print("=" * 50)
    print("\nThis will help you create a cookies.txt file for Instagram downloads.")
    print("\nOption 1: Use a browser extension (recommended)")
    print("-" * 40)
    print("1. Install 'Get cookies.txt LOCALLY' extension")
    print("   Chrome: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc")
    print("   Firefox: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/")
    print("2. Log into Instagram in your browser")
    print("3. Click the extension icon while on Instagram")
    print("4. Save as 'instagram_cookies.txt'")
    print("5. Use: ./media-downloader.py --cookies instagram_cookies.txt [URL]")
    
    print("\nOption 2: Manual cookie export")
    print("-" * 40)
    print("1. Log into Instagram in your browser")
    print("2. Open Developer Tools (F12)")
    print("3. Go to Application/Storage tab → Cookies → instagram.com")
    print("4. Look for these important cookies:")
    print("   - sessionid (most important)")
    print("   - csrftoken")
    print("   - ds_user_id")
    print("5. Create a cookies.txt file with this format:")
    print("\n# Netscape HTTP Cookie File")
    print(".instagram.com\tTRUE\t/\tTRUE\t0\tsessionid\t[YOUR_SESSION_ID]")
    print(".instagram.com\tTRUE\t/\tTRUE\t0\tcsrftoken\t[YOUR_CSRF_TOKEN]")
    print(".instagram.com\tTRUE\t/\tTRUE\t0\tds_user_id\t[YOUR_USER_ID]")
    
    print("\nExample usage:")
    print("-" * 40)
    print("./media-downloader.py -v --cookies instagram_cookies.txt https://www.instagram.com/stories/[username]/[story_id]/")
    print("\nNote: Cookies expire, so you may need to re-export them periodically.")

if __name__ == "__main__":
    create_cookie_file()