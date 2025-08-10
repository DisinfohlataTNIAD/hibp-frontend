#!/usr/bin/env python3
"""
Test script untuk DeHashed v2 API sesuai dokumentasi
"""

import requests
import hashlib

api_key = "7AG14cikiWpWmLbU0TdsJXGEGE26r+1iAooR2/f7wgHHzItdVLUSPek="

def get_sha256(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def v2_search_password(password: str) -> dict:
    """Test password search sesuai dokumentasi"""
    sha256_hash = get_sha256(password)
    res = requests.post("https://api.dehashed.com/v2/search-password", json={
        "sha256_hashed_password": sha256_hash,
    }, headers={
        "Content-Type": "application/json",
        "DeHashed-Api-Key": api_key,
    })
    return res.json()

def v2_search_email(email: str) -> dict:
    """Test email search dengan v2 API"""
    res = requests.post("https://api.dehashed.com/v2/search", json={
        "query": f"email:{email}",
        "size": 10
    }, headers={
        "Content-Type": "application/json",
        "DeHashed-Api-Key": api_key,
    })
    return res.json()

if __name__ == '__main__':
    print("🔍 Testing DeHashed v2 API...")
    print("=" * 50)
    
    # Test 1: Password search
    print("1. Testing password search...")
    try:
        response = v2_search_password("Password12345")
        print(f"Password search result: {response}")
    except Exception as e:
        print(f"Password search error: {e}")
    
    print("\n" + "-" * 30)
    
    # Test 2: Email search
    print("2. Testing email search...")
    try:
        response = v2_search_email("test@gmail.com")
        print(f"Email search result: {response}")
    except Exception as e:
        print(f"Email search error: {e}")
    
    print("\n" + "-" * 30)
    
    # Test 3: Check API key validity
    print("3. Testing API key validity...")
    try:
        res = requests.post("https://api.dehashed.com/v2/search", json={
            "query": "email:nonexistent@example.com",
            "size": 1
        }, headers={
            "Content-Type": "application/json",
            "DeHashed-Api-Key": api_key,
        })
        print(f"API key test - Status: {res.status_code}")
        if res.status_code == 200:
            print("✅ API key is valid!")
        elif res.status_code == 401:
            print("❌ API key is invalid or expired")
        elif res.status_code == 403:
            print("⚠️ API key valid but access forbidden")
        else:
            print(f"⚠️ Unexpected status: {res.status_code}")
            print(f"Response: {res.text}")
    except Exception as e:
        print(f"API key test error: {e}")
