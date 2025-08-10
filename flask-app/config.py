#!/usr/bin/env python3
"""
Configuration file untuk Breach Checker
Semua kredensial dan pengaturan disimpan di sini
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # Rate Limiting
    RATE_LIMIT_DELAY = 1  # seconds between API calls
    REQUEST_TIMEOUT = 10  # seconds
    MAX_RETRIES = 3
    
    # Local Database
    LOCAL_BREACH_FILE = 'local_breaches.txt'
    
class APICredentials:
    """API credentials and endpoints"""
    
    # DeHashed API Configuration
    DEHASHED = {
        'api_key': '7AG14cikiWpWmLbU0TdsJXGEGE26r+1iAooR2/f7wgHHzItdVLUSPek=',
        'base_url': 'https://api.dehashed.com',
        'endpoints': {
            'search': '/v2/search',
            'search_password': '/v2/search-password'
        },
        'enabled': True,
        'free_tier_limit': 10,
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'BreachChecker/1.0'
        }
    }
    
    # Intelligence X API Configuration
    INTELX = {
        'api_key': os.environ.get('INTELX_API_KEY', 'YOUR_INTELX_API_KEY'),
        'base_url': 'https://2.intelx.io',
        'endpoints': {
            'search': '/phonebook/search'
        },
        'enabled': False,  # Set True when API key is provided
        'free_tier_limit': 50
    }
    
    # HIBP Configuration
    HIBP = {
        'base_url': 'https://api.pwnedpasswords.com',
        'breaches_url': 'https://haveibeenpwned.com/api/v3',
        'endpoints': {
            'password_range': '/range/',
            'breached_account': '/breachedaccount/'
        },
        'enabled': True,
        'free': True
    }

class DatabaseConfig:
    """Database and storage configuration"""
    
    # Local breach database
    LOCAL_DB = {
        'file': 'local_breaches.txt',
        'encoding': 'utf-8',
        'case_sensitive': False,
        'auto_backup': True,
        'backup_interval': 86400  # 24 hours
    }
    
    # Statistics storage
    STATS = {
        'file': 'stats.json',
        'update_interval': 300,  # 5 minutes
        'keep_history': True
    }

class SecurityConfig:
    """Security and privacy settings"""
    
    # Password hashing
    PASSWORD_HASH_ALGORITHM = 'sha1'  # For HIBP compatibility
    DEHASHED_HASH_ALGORITHM = 'sha256'  # For DeHashed API
    
    # Privacy settings
    LOG_QUERIES = False  # Don't log actual queries for privacy
    STORE_RESULTS = False  # Don't store breach results
    ANONYMIZE_LOGS = True
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']
    
    # Rate limiting
    RATE_LIMITS = {
        'per_minute': 60,
        'per_hour': 1000,
        'per_day': 10000
    }

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    LOCAL_BREACH_FILE = 'test_breaches.txt'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])

def validate_config() -> Dict[str, Any]:
    """Validate configuration and return status"""
    status = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'api_status': {}
    }
    
    # Check DeHashed API key
    if APICredentials.DEHASHED['api_key'] == 'YOUR_DEHASHED_API_KEY':
        status['warnings'].append('DeHashed API key not configured')
        status['api_status']['dehashed'] = 'not_configured'
    else:
        status['api_status']['dehashed'] = 'configured'
    
    # Check Intelligence X API key
    if APICredentials.INTELX['api_key'] == 'YOUR_INTELX_API_KEY':
        status['warnings'].append('Intelligence X API key not configured')
        status['api_status']['intelx'] = 'not_configured'
    else:
        status['api_status']['intelx'] = 'configured'
    
    # Check local database file
    if os.path.exists(DatabaseConfig.LOCAL_DB['file']):
        status['api_status']['local_db'] = 'available'
    else:
        status['warnings'].append('Local breach database not found')
        status['api_status']['local_db'] = 'missing'
    
    # HIBP is always available
    status['api_status']['hibp'] = 'available'
    
    return status

if __name__ == '__main__':
    # Test configuration
    print("🔧 Configuration Test")
    print("=" * 30)
    
    config_status = validate_config()
    print(f"Configuration valid: {config_status['valid']}")
    
    if config_status['errors']:
        print("❌ Errors:")
        for error in config_status['errors']:
            print(f"  - {error}")
    
    if config_status['warnings']:
        print("⚠️ Warnings:")
        for warning in config_status['warnings']:
            print(f"  - {warning}")
    
    print("\n📊 API Status:")
    for api, status in config_status['api_status'].items():
        emoji = "✅" if status in ['available', 'configured'] else "⚠️"
        print(f"  {emoji} {api}: {status}")
