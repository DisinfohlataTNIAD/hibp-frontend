#!/usr/bin/env python3
"""
API Client classes untuk berbagai sumber data breach
Memisahkan logic API dari breach checker utama
"""

import requests
import hashlib
import time
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from config import APICredentials, Config

class BaseAPIClient(ABC):
    """Base class untuk semua API clients"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BreachChecker/1.0'
        })
    
    @abstractmethod
    def check_email(self, email: str) -> Dict:
        """Check email breach"""
        pass
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        try:
            kwargs.setdefault('timeout', Config.REQUEST_TIMEOUT)
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

class HIBPClient(BaseAPIClient):
    """Client untuk Have I Been Pwned API"""
    
    def __init__(self):
        super().__init__()
        self.base_url = APICredentials.HIBP['base_url']
        self.breaches_url = APICredentials.HIBP['breaches_url']
    
    def check_password(self, password: str) -> Dict:
        """Check password menggunakan k-anonymity"""
        try:
            # Hash password dengan SHA-1
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            # Query API dengan prefix saja (k-anonymity)
            url = f"{self.base_url}/range/{prefix}"
            response = self._make_request('GET', url)
            
            if response.status_code == 200:
                # Cari suffix dalam response
                for line in response.text.split('\n'):
                    if line.startswith(suffix):
                        count = int(line.split(':')[1])
                        return {
                            'pwned': True,
                            'count': count,
                            'message': f'Password ditemukan dalam {count} breach',
                            'status': 'found',
                            'source': 'HIBP'
                        }
                
                return {
                    'pwned': False,
                    'count': 0,
                    'message': 'Password tidak ditemukan dalam database',
                    'status': 'clean',
                    'source': 'HIBP'
                }
            else:
                return {
                    'error': f'HIBP API error: HTTP {response.status_code}',
                    'status': 'api_error',
                    'source': 'HIBP'
                }
            
        except Exception as e:
            return {
                'error': f'Error checking password: {str(e)}',
                'status': 'exception',
                'source': 'HIBP'
            }
    
    def check_email(self, email: str) -> Dict:
        """Check email breaches (rate limited)"""
        try:
            url = f"{self.breaches_url}/breachedaccount/{email}"
            headers = {
                'Accept': 'application/json'
            }
            
            response = self._make_request('GET', url, headers=headers)
            
            if response.status_code == 200:
                breaches = response.json()
                return {
                    'found': True,
                    'breaches': breaches,
                    'total': len(breaches),
                    'message': f'Found {len(breaches)} breaches in HIBP',
                    'status': 'found',
                    'source': 'HIBP'
                }
            elif response.status_code == 404:
                return {
                    'found': False,
                    'message': 'Email tidak ditemukan dalam HIBP database',
                    'status': 'clean',
                    'source': 'HIBP'
                }
            elif response.status_code == 429:
                return {
                    'error': 'HIBP rate limit exceeded. Try again later.',
                    'status': 'rate_limited',
                    'source': 'HIBP'
                }
            elif response.status_code == 401:
                return {
                    'error': 'HIBP API requires authentication for this request',
                    'status': 'auth_required',
                    'source': 'HIBP'
                }
            else:
                return {
                    'error': f'HIBP API error: HTTP {response.status_code}',
                    'status': 'api_error',
                    'source': 'HIBP'
                }
                
        except Exception as e:
            return {
                'error': f'Error with HIBP API: {str(e)}',
                'status': 'exception',
                'source': 'HIBP'
            }

class DeHashedClient(BaseAPIClient):
    """Client untuk DeHashed API v2"""
    
    def __init__(self):
        super().__init__()
        self.config = APICredentials.DEHASHED
        self.base_url = self.config['base_url']
        self.api_key = self.config['api_key']
    
    def _get_headers(self) -> Dict:
        """Get headers untuk DeHashed API"""
        headers = self.config['headers'].copy()
        headers['DeHashed-Api-Key'] = self.api_key
        return headers
    
    def check_email(self, email: str) -> Dict:
        """Check email menggunakan DeHashed v2 API"""
        try:
            if not self.config['enabled'] or self.api_key == 'YOUR_DEHASHED_API_KEY':
                return {
                    'error': 'DeHashed API not configured',
                    'status': 'not_configured',
                    'source': 'DeHashed'
                }
            
            url = f"{self.base_url}{self.config['endpoints']['search']}"
            payload = {
                "query": f"email:{email}",
                "size": self.config['free_tier_limit']
            }
            
            response = self._make_request('POST', url, json=payload, headers=self._get_headers())
            
            if response.status_code == 200:
                data = response.json()
                entries = data.get('entries', [])
                return {
                    'found': len(entries) > 0,
                    'breaches': entries,
                    'total': data.get('total', 0),
                    'message': f"Found {data.get('total', 0)} entries in DeHashed",
                    'status': 'success',
                    'source': 'DeHashed',
                    'api_version': 'v2'
                }
            elif response.status_code == 401:
                # Check if it's subscription issue
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', '')
                    if 'subscription' in error_msg.lower():
                        return {
                            'error': 'DeHashed email search requires paid subscription',
                            'status': 'subscription_required',
                            'source': 'DeHashed',
                            'note': 'Password search still works with current API key'
                        }
                except:
                    pass
                
                return {
                    'error': 'DeHashed API authentication failed',
                    'status': 'auth_failed',
                    'source': 'DeHashed'
                }
            elif response.status_code == 429:
                return {
                    'error': 'DeHashed rate limit exceeded',
                    'status': 'rate_limited',
                    'source': 'DeHashed'
                }
            else:
                return {
                    'error': f'DeHashed API error: HTTP {response.status_code}',
                    'status': 'api_error',
                    'source': 'DeHashed',
                    'response_text': response.text[:200] if response.text else 'No response'
                }
            
        except Exception as e:
            return {
                'error': f'Error with DeHashed: {str(e)}',
                'status': 'exception',
                'source': 'DeHashed'
            }
    
    def check_password(self, password: str) -> Dict:
        """Check password menggunakan DeHashed v2 API"""
        try:
            if not self.config['enabled'] or self.api_key == 'YOUR_DEHASHED_API_KEY':
                return {
                    'error': 'DeHashed API not configured',
                    'status': 'not_configured',
                    'source': 'DeHashed'
                }
            
            # Hash password dengan SHA256
            sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            
            url = f"{self.base_url}{self.config['endpoints']['search_password']}"
            payload = {
                "sha256_hashed_password": sha256_hash
            }
            
            response = self._make_request('POST', url, json=payload, headers=self._get_headers())
            
            if response.status_code == 200:
                data = response.json()
                results_found = data.get('results_found', 0)
                return {
                    'found': results_found > 0,
                    'count': results_found,
                    'message': f"Password found in {results_found} DeHashed entries",
                    'status': 'success',
                    'source': 'DeHashed',
                    'api_version': 'v2'
                }
            elif response.status_code == 401:
                return {
                    'error': 'DeHashed API authentication failed',
                    'status': 'auth_failed',
                    'source': 'DeHashed'
                }
            elif response.status_code == 429:
                return {
                    'error': 'DeHashed rate limit exceeded',
                    'status': 'rate_limited',
                    'source': 'DeHashed'
                }
            else:
                return {
                    'error': f'DeHashed password API error: HTTP {response.status_code}',
                    'status': 'api_error',
                    'source': 'DeHashed'
                }
                
        except Exception as e:
            return {
                'error': f'Error with DeHashed password check: {str(e)}',
                'status': 'exception',
                'source': 'DeHashed'
            }

class IntelligenceXClient(BaseAPIClient):
    """Client untuk Intelligence X API"""
    
    def __init__(self):
        super().__init__()
        self.config = APICredentials.INTELX
        self.base_url = self.config['base_url']
        self.api_key = self.config['api_key']
    
    def check_email(self, email: str) -> Dict:
        """Check email menggunakan Intelligence X API"""
        try:
            if not self.config['enabled'] or self.api_key == 'YOUR_INTELX_API_KEY':
                return {
                    'error': 'Intelligence X API key not configured',
                    'status': 'not_configured',
                    'source': 'IntelligenceX'
                }
            
            url = f"{self.base_url}{self.config['endpoints']['search']}"
            data = {
                'term': email,
                'maxresults': self.config['free_tier_limit'],
                'media': 0,
                'target': 1
            }
            
            headers = {
                'x-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = self._make_request('POST', url, json=data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                selectors = result.get('selectors', [])
                return {
                    'found': len(selectors) > 0,
                    'results': selectors,
                    'total': len(selectors),
                    'message': f"Found {len(selectors)} results in Intelligence X",
                    'status': 'success',
                    'source': 'IntelligenceX'
                }
            else:
                return {
                    'error': f'Intelligence X API error: HTTP {response.status_code}',
                    'status': 'api_error',
                    'source': 'IntelligenceX'
                }
            
        except Exception as e:
            return {
                'error': f'Error with Intelligence X: {str(e)}',
                'status': 'exception',
                'source': 'IntelligenceX'
            }

class LocalDatabaseClient:
    """Client untuk local breach database"""
    
    def __init__(self):
        from config import DatabaseConfig
        self.config = DatabaseConfig.LOCAL_DB
        self.file_path = self.config['file']
    
    def check_email(self, email: str) -> Dict:
        """Check email terhadap database lokal"""
        try:
            try:
                with open(self.file_path, 'r', encoding=self.config['encoding']) as f:
                    breached_emails = f.read().splitlines()
                
                # Case insensitive comparison if configured
                if not self.config['case_sensitive']:
                    email_lower = email.lower()
                    found = email_lower in [e.lower() for e in breached_emails]
                else:
                    found = email in breached_emails
                
                if found:
                    return {
                        'found': True,
                        'message': 'Email ditemukan dalam database breach lokal',
                        'status': 'found',
                        'source': 'LocalDB'
                    }
                else:
                    return {
                        'found': False,
                        'message': 'Email tidak ditemukan dalam database lokal',
                        'status': 'clean',
                        'source': 'LocalDB'
                    }
                    
            except FileNotFoundError:
                return {
                    'error': f'Local breach database not found: {self.file_path}',
                    'status': 'db_missing',
                    'source': 'LocalDB'
                }
                
        except Exception as e:
            return {
                'error': f'Error checking local database: {str(e)}',
                'status': 'exception',
                'source': 'LocalDB'
            }
    
    def add_email(self, email: str) -> bool:
        """Add email to local database"""
        try:
            with open(self.file_path, 'a', encoding=self.config['encoding']) as f:
                f.write(f"{email}\n")
            return True
        except Exception:
            return False
    
    def get_stats(self) -> Dict:
        """Get statistics about local database"""
        try:
            with open(self.file_path, 'r', encoding=self.config['encoding']) as f:
                emails = f.read().splitlines()
            
            return {
                'total_emails': len(emails),
                'unique_emails': len(set(emails)),
                'file_size': os.path.getsize(self.file_path),
                'last_modified': os.path.getmtime(self.file_path)
            }
        except Exception as e:
            return {
                'error': str(e),
                'total_emails': 0
            }
