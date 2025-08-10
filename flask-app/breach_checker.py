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
from api_config import DEHASHED_CONFIG, INTELX_CONFIG, LOCAL_DB_CONFIG, HIBP_CONFIG

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
        Check menggunakan DeHashed API v2 - Email search memerlukan subscription
        """
        try:
            api_key = "7AG14cikiWpWmLbU0TdsJXGEGE26r+1iAooR2/f7wgHHzItdVLUSPek="
            
            if not api_key or api_key == "YOUR_DEHASHED_API_KEY":
                return {
                    'error': 'DeHashed API key belum diset'
                }
            
            # DeHashed v2 API endpoint untuk email search
            url = "https://api.dehashed.com/v2/search"
            
            # Payload untuk email search (JSON format)
            payload = {
                "query": f"email:{email}",
                "size": 10  # Limit untuk free tier
            }
            
            headers = {
                "Content-Type": "application/json",
                "DeHashed-Api-Key": api_key,
                "User-Agent": "BreachChecker/1.0"
            }
            
            response = self.session.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                entries = data.get('entries', [])
                return {
                    'found': len(entries) > 0,
                    'breaches': entries,
                    'total': data.get('total', 0),
                    'message': f"Found {data.get('total', 0)} entries in DeHashed v2",
                    'status': 'success',
                    'api_version': 'v2'
                }
            elif response.status_code == 401:
                # Check if it's subscription issue
                try:
                    error_data = response.json()
                    if 'subscription' in error_data.get('error', '').lower():
                        return {
                            'error': 'DeHashed email search requires paid subscription',
                            'status': 'subscription_required',
                            'api_version': 'v2',
                            'note': 'Password search still works with current API key'
                        }
                except:
                    pass
                
                return {
                    'error': 'DeHashed API authentication failed. Check API key.',
                    'status': 'auth_failed',
                    'api_version': 'v2'
                }
            elif response.status_code == 429:
                return {
                    'error': 'DeHashed rate limit exceeded. Try again later.',
                    'status': 'rate_limited'
                }
            elif response.status_code == 403:
                return {
                    'error': 'DeHashed API access forbidden. Check account status.',
                    'status': 'forbidden'
                }
            else:
                # Try to get error message from response
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', f'HTTP {response.status_code}')
                    
                    if 'subscription' in error_msg.lower():
                        return {
                            'error': 'DeHashed email search requires paid subscription',
                            'status': 'subscription_required',
                            'api_version': 'v2',
                            'details': error_msg
                        }
                except:
                    pass
                
                return {
                    'error': f'DeHashed v2 API error: HTTP {response.status_code}',
                    'status': 'api_error',
                    'response_text': response.text[:200] if response.text else 'No response',
                    'api_version': 'v2'
                }
            
        except Exception as e:
            return {
                'error': f'Error with DeHashed v2: {str(e)}',
                'status': 'exception'
            }
            
        except Exception as e:
            return {'error': f'Error with DeHashed: {str(e)}'}
    
    def check_dehashed_password(self, password: str) -> Dict:
        """
        Check password menggunakan DeHashed v2 API (sesuai dokumentasi)
        """
        try:
            api_key = "7AG14cikiWpWmLbU0TdsJXGEGE26r+1iAooR2/f7wgHHzItdVLUSPek="
            
            def get_sha256(password: str) -> str:
                return hashlib.sha256(password.encode('utf-8')).hexdigest()
            
            sha256_hash = get_sha256(password)
            
            url = "https://api.dehashed.com/v2/search-password"
            payload = {
                "sha256_hashed_password": sha256_hash
            }
            
            headers = {
                "Content-Type": "application/json",
                "DeHashed-Api-Key": api_key,
                "User-Agent": "BreachChecker/1.0"
            }
            
            response = self.session.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                entries = data.get('entries', [])
                return {
                    'found': len(entries) > 0,
                    'breaches': entries,
                    'total': len(entries),
                    'message': f"Password found in {len(entries)} DeHashed entries",
                    'status': 'success',
                    'api_version': 'v2'
                }
            elif response.status_code == 401:
                return {
                    'error': 'DeHashed API authentication failed',
                    'status': 'auth_failed'
                }
            elif response.status_code == 429:
                return {
                    'error': 'DeHashed rate limit exceeded',
                    'status': 'rate_limited'
                }
            else:
                return {
                    'error': f'DeHashed password API error: HTTP {response.status_code}',
                    'status': 'api_error',
                    'response_text': response.text[:200] if response.text else 'No response'
                }
                
        except Exception as e:
            return {
                'error': f'Error with DeHashed password check: {str(e)}',
                'status': 'exception'
            }
    
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
            print("Checking password with HIBP...")
            results['password_check'] = self.check_pwned_passwords(password)
            time.sleep(1)  # Rate limiting
            
            # Also check with DeHashed password search (works with current API key)
            print("Checking password with DeHashed...")
            dehashed_pwd_result = self.check_dehashed_password(password)
            if dehashed_pwd_result.get('status') == 'success':
                results['password_check_dehashed'] = dehashed_pwd_result
            time.sleep(1)
        
        # Check berbagai sumber untuk email
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
