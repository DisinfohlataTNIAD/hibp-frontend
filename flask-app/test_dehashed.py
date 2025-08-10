#!/usr/bin/env python3
"""
Test script untuk DeHashed API
"""

import requests
import base64

def test_dehashed_api():
    # DeHashed credentials
    api_email = "your-email@example.com"  # Ganti dengan email DeHashed Anda
    api_key = "7AG14cikiWpWmLbU0TdsJXGEGE26r+1iAooR2/f7wgHHzItdVLUSPek="
    
    # Test email
    test_email = "test@example.com"
    
    print("🔍 Testing DeHashed API...")
    print(f"Email: {api_email}")
    print(f"API Key: {api_key[:20]}...")
    print(f"Test Query: {test_email}")
    print("-" * 50)
    
    try:
        # Prepare request
        url = "https://api.dehashed.com/search"
        params = {
            'query': f'email:{test_email}',
            'size': 5
        }
        
        # Basic Auth
        credentials = f"{api_email}:{api_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_credentials}',
            'User-Agent': 'BreachChecker/1.0'
        }
        
        print("📡 Making API request...")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Request Successful!")
            print(f"Total Results: {data.get('total', 0)}")
            print(f"Entries: {len(data.get('entries', []))}")
            
            if data.get('entries'):
                print("\n📋 Sample Results:")
                for i, entry in enumerate(data.get('entries', [])[:3]):
                    print(f"  {i+1}. {entry}")
            else:
                print("No entries found for test email")
                
        elif response.status_code == 401:
            print("❌ Authentication Failed!")
            print("Check your email and API key")
            
        elif response.status_code == 429:
            print("⚠️ Rate Limited!")
            print("Too many requests, try again later")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_dehashed_api()
