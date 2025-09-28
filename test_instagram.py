#!/usr/bin/env python3

import re

def is_profile_url(url):
    """Check if URL is an Instagram profile URL"""
    pattern = r'^(https?://)?(www\.)?instagram\.com/([^/]+)/?$'
    match = re.match(pattern, url)
    if match:
        username = match.group(3)
        special_pages = ['p', 'reel', 'tv', 'stories', 'explore', 'accounts', 'about', 'legal', 'privacy']
        return username not in special_pages
    return False

def extract_username(url):
    """Extract username from Instagram profile URL"""
    pattern = r'^(https?://)?(www\.)?instagram\.com/([^/]+)/?$'
    match = re.match(pattern, url)
    if match:
        return match.group(3)
    return None

# Test URLs
test_urls = [
    'https://www.instagram.com/drmbt',
    'https://www.instagram.com/drmbt/',
    'instagram.com/drmbt',
    'https://www.instagram.com/p/ABC123',
    'https://www.instagram.com/reel/XYZ789',
]

for url in test_urls:
    print(f"URL: {url}")
    print(f"  Is profile: {is_profile_url(url)}")
    print(f"  Username: {extract_username(url)}")
    print()