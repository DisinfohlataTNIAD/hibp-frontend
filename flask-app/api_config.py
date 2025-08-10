#!/usr/bin/env python3
"""
API Configuration untuk Breach Checker
Ganti credentials di sini sesuai dengan akun Anda
"""

# DeHashed API Configuration
DEHASHED_CONFIG = {
    'email': 'your-email@example.com',  # GANTI dengan email DeHashed Anda
    'api_key': '7AG14cikiWpWmLbU0TdsJXGEGE26r+1iAooR2/f7wgHHzItdVLUSPek=',
    'enabled': False  # Set True setelah email diupdate
}

# Intelligence X API Configuration  
INTELX_CONFIG = {
    'api_key': 'YOUR_INTELX_API_KEY',
    'enabled': False
}

# Local Database Configuration
LOCAL_DB_CONFIG = {
    'file': 'local_breaches.txt',
    'enabled': True
}

# HIBP Configuration (selalu aktif, gratis)
HIBP_CONFIG = {
    'enabled': True,
    'endpoint': 'https://api.pwnedpasswords.com/range/'
}
