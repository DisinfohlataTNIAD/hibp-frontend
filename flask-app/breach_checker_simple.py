#!/usr/bin/env python3
"""
Simplified Breach Checker - Focus on working sources
"""

import requests
import hashlib
import time
import json
from typing import Dict, List, Optional

class SimpleBreachChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
        })
    
    def check_pwned_passwords(self, password: str) -> Dict:
        """
        Check password menggunakan HIBP Pwned Passwords API (100% gratis)
        """
        try:
            # Hash password dengan SHA-1
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            # Query API dengan prefix saja (k-anonymity)
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Cari suffix dalam response
                for line in response.text.split('\n'):
                    if line.startswith(suffix):
                        count = int(line.split(':')[1])
                        return {
                            'pwned': True,
                            'count': count,
                            'message': f'Password ditemukan dalam {count} breach',
                            'status': 'found'
                        }
                
                return {
                    'pwned': False,
                    'count': 0,
                    'message': 'Password tidak ditemukan dalam database',
                    'status': 'clean'
                }
            else:
                return {
                    'error': f'HIBP API error: HTTP {response.status_code}',
                    'status': 'api_error'
                }
            
        except Exception as e:
            return {
                'error': f'Error checking password: {str(e)}',
                'status': 'exception'
            }
    
    def check_local_breach_db(self, email: str) -> Dict:
        """
        Check terhadap database breach lokal
        """
        try:
            breach_file = "local_breaches.txt"
            
            try:
                with open(breach_file, 'r') as f:
                    breached_emails = f.read().splitlines()
                    
                if email.lower() in [e.lower() for e in breached_emails]:
                    return {
                        'found': True,
                        'source': 'Local Database',
                        'message': 'Email ditemukan dalam database breach lokal',
                        'status': 'found'
                    }
                else:
                    return {
                        'found': False,
                        'message': 'Email tidak ditemukan dalam database lokal',
                        'status': 'clean'
                    }
                    
            except FileNotFoundError:
                return {
                    'error': 'Database breach lokal tidak ditemukan',
                    'status': 'db_missing'
                }
                
        except Exception as e:
            return {
                'error': f'Error checking local database: {str(e)}',
                'status': 'exception'
            }
    
    def check_haveibeenpwned_api(self, email: str) -> Dict:
        """
        Check menggunakan HIBP API (rate limited, tapi gratis untuk beberapa query)
        """
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {
                'User-Agent': 'BreachChecker/1.0',
                'Accept': 'application/json'
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                return {
                    'found': True,
                    'breaches': breaches,
                    'total': len(breaches),
                    'message': f'Found {len(breaches)} breaches in HIBP',
                    'status': 'found'
                }
            elif response.status_code == 404:
                return {
                    'found': False,
                    'message': 'Email tidak ditemukan dalam HIBP database',
                    'status': 'clean'
                }
            elif response.status_code == 429:
                return {
                    'error': 'HIBP rate limit exceeded. Try again later.',
                    'status': 'rate_limited'
                }
            elif response.status_code == 401:
                return {
                    'error': 'HIBP API requires authentication for this request',
                    'status': 'auth_required'
                }
            else:
                return {
                    'error': f'HIBP API error: HTTP {response.status_code}',
                    'status': 'api_error'
                }
                
        except Exception as e:
            return {
                'error': f'Error with HIBP API: {str(e)}',
                'status': 'exception'
            }
    
    def comprehensive_check(self, email: str, password: str = None) -> Dict:
        """
        Check komprehensif menggunakan sumber yang reliable
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
            time.sleep(0.5)  # Rate limiting
        
        # Check local database (selalu cepat)
        print("Checking local database...")
        results['sources']['local'] = self.check_local_breach_db(email)
        time.sleep(0.5)
        
        # Check HIBP API (mungkin rate limited)
        print("Checking HIBP API...")
        results['sources']['hibp'] = self.check_haveibeenpwned_api(email)
        time.sleep(1)  # HIBP rate limiting
        
        # Add DeHashed status (disabled)
        results['sources']['dehashed'] = {
            'error': 'DeHashed API temporarily disabled. Check credentials.',
            'status': 'disabled',
            'note': 'API key provided but authentication failed'
        }
        
        return results

def main():
    """
    Test the simplified breach checker
    """
    checker = SimpleBreachChecker()
    
    test_email = "test@example.com"
    test_password = "password123"
    
    print("=== Simplified Breach Checker ===")
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
        if result.get('found'):
            print(f"⚠️  {source.upper()}: BREACH DETECTED")
            breach_found = True
        elif result.get('status') == 'clean':
            print(f"✅ {source.upper()}: Clean")
        elif result.get('status') == 'disabled':
            print(f"⚪ {source.upper()}: Disabled")
        elif 'error' in result:
            print(f"❌ {source.upper()}: {result['error']}")
    
    if not breach_found:
        print("\n🎉 Email tidak ditemukan dalam database breach yang dicek!")

if __name__ == "__main__":
    main()
