#!/usr/bin/env python3
"""
Free Breach Checker - Alternative to HIBP
Menggunakan berbagai sumber data gratis untuk check email breach
"""

import requests
import hashlib
import time
import json
from typing import Dict, List, Optional

class BreachChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
        })
    
    def check_pwned_passwords(self, password: str) -> Dict:
        """
        Check password menggunakan HIBP Pwned Passwords API (masih gratis)
        Menggunakan k-anonymity model
        """
        try:
            # Hash password dengan SHA-1
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            # Query API dengan prefix saja (k-anonymity)
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                # Cari suffix dalam response
                for line in response.text.split('\n'):
                    if line.startswith(suffix):
                        count = int(line.split(':')[1])
                        return {
                            'pwned': True,
                            'count': count,
                            'message': f'Password ditemukan dalam {count} breach'
                        }
                
                return {
                    'pwned': False,
                    'count': 0,
                    'message': 'Password tidak ditemukan dalam database'
                }
            
        except Exception as e:
            return {'error': f'Error checking password: {str(e)}'}
    
    def check_dehashed_free(self, email: str) -> Dict:
        """
        Check menggunakan DeHashed free tier (perlu API key gratis)
        """
        try:
            # Note: Perlu daftar untuk dapat API key gratis
            api_key = "YOUR_DEHASHED_API_KEY"  # Ganti dengan API key Anda
            
            if api_key == "YOUR_DEHASHED_API_KEY":
                return {
                    'error': 'DeHashed API key belum diset. Daftar di dehashed.com untuk API key gratis'
                }
            
            url = "https://api.dehashed.com/search"
            params = {
                'query': f'email:{email}',
                'size': 10  # Limit untuk free tier
            }
            
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Basic {api_key}'
            }
            
            response = self.session.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'found': len(data.get('entries', [])) > 0,
                    'breaches': data.get('entries', []),
                    'total': data.get('total', 0)
                }
            
        except Exception as e:
            return {'error': f'Error with DeHashed: {str(e)}'}
    
    def check_intelligence_x(self, email: str) -> Dict:
        """
        Check menggunakan Intelligence X (ada free tier)
        """
        try:
            # Note: Perlu API key dari intelx.io
            api_key = "YOUR_INTELX_API_KEY"
            
            if api_key == "YOUR_INTELX_API_KEY":
                return {
                    'error': 'Intelligence X API key belum diset. Daftar di intelx.io'
                }
            
            url = "https://2.intelx.io/phonebook/search"
            data = {
                'term': email,
                'maxresults': 10,
                'media': 0,
                'target': 1
            }
            
            headers = {
                'x-key': api_key,
                'Content-Type': 'application/json'
            }
            
            response = self.session.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'found': len(result.get('selectors', [])) > 0,
                    'results': result.get('selectors', [])
                }
            
        except Exception as e:
            return {'error': f'Error with Intelligence X: {str(e)}'}
    
    def check_local_breach_db(self, email: str) -> Dict:
        """
        Check terhadap database breach lokal (jika ada)
        """
        try:
            # Contoh implementasi untuk database lokal
            # Anda bisa download dataset breach dan simpan lokal
            
            breach_file = "local_breaches.txt"  # File berisi email yang breach
            
            try:
                with open(breach_file, 'r') as f:
                    breached_emails = f.read().splitlines()
                    
                if email.lower() in [e.lower() for e in breached_emails]:
                    return {
                        'found': True,
                        'source': 'Local Database',
                        'message': 'Email ditemukan dalam database breach lokal'
                    }
                else:
                    return {
                        'found': False,
                        'message': 'Email tidak ditemukan dalam database lokal'
                    }
                    
            except FileNotFoundError:
                return {
                    'error': 'Database breach lokal tidak ditemukan. Buat file local_breaches.txt'
                }
                
        except Exception as e:
            return {'error': f'Error checking local database: {str(e)}'}
    
    def comprehensive_check(self, email: str, password: str = None) -> Dict:
        """
        Check komprehensif menggunakan semua sumber yang tersedia
        """
        results = {
            'email': email,
            'timestamp': time.time(),
            'sources': {}
        }
        
        print(f"Checking {email}...")
        
        # Check password jika disediakan
        if password:
            print("Checking password...")
            results['password_check'] = self.check_pwned_passwords(password)
            time.sleep(1)  # Rate limiting
        
        # Check berbagai sumber
        print("Checking DeHashed...")
        results['sources']['dehashed'] = self.check_dehashed_free(email)
        time.sleep(1)
        
        print("Checking Intelligence X...")
        results['sources']['intelx'] = self.check_intelligence_x(email)
        time.sleep(1)
        
        print("Checking local database...")
        results['sources']['local'] = self.check_local_breach_db(email)
        
        return results

def main():
    """
    Contoh penggunaan
    """
    checker = BreachChecker()
    
    # Test email
    test_email = "test@example.com"
    test_password = "password123"  # Jangan gunakan password asli!
    
    print("=== Free Breach Checker ===")
    print(f"Checking: {test_email}")
    print("-" * 40)
    
    results = checker.comprehensive_check(test_email, test_password)
    
    # Print hasil
    print("\n=== HASIL ===")
    print(json.dumps(results, indent=2, default=str))
    
    # Summary
    print("\n=== SUMMARY ===")
    if 'password_check' in results:
        pwd_result = results['password_check']
        if pwd_result.get('pwned'):
            print(f"⚠️  Password: PWNED ({pwd_result.get('count')} kali)")
        else:
            print("✅ Password: Aman")
    
    breach_found = False
    for source, result in results['sources'].items():
        if result.get('found') or result.get('pwned'):
            print(f"⚠️  {source}: BREACH DETECTED")
            breach_found = True
        elif 'error' not in result:
            print(f"✅ {source}: Clean")
    
    if not breach_found:
        print("\n🎉 Email tidak ditemukan dalam database breach yang dicek!")

if __name__ == "__main__":
    main()
