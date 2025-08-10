#!/usr/bin/env python3
"""
Refactored Breach Checker - Clean architecture dengan API clients terpisah
"""

import time
import json
from typing import Dict, List, Optional
from datetime import datetime

from config import Config, validate_config
from api_clients import (
    HIBPClient, 
    DeHashedClient, 
    IntelligenceXClient, 
    LocalDatabaseClient
)

class BreachChecker:
    """Main breach checker class dengan clean architecture"""
    
    def __init__(self):
        self.config = Config()
        self.config_status = validate_config()
        
        # Initialize API clients
        self.hibp_client = HIBPClient()
        self.dehashed_client = DeHashedClient()
        self.intelx_client = IntelligenceXClient()
        self.local_client = LocalDatabaseClient()
        
        # Statistics
        self.stats = {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'last_check': None
        }
    
    def check_password(self, password: str) -> Dict:
        """
        Comprehensive password checking menggunakan multiple sources
        """
        results = {
            'password_hash': '***hidden***',  # Don't log actual password
            'timestamp': time.time(),
            'sources': {}
        }
        
        print("Checking password with multiple sources...")
        
        # Check with HIBP (always available)
        print("- Checking HIBP...")
        results['sources']['hibp'] = self.hibp_client.check_password(password)
        time.sleep(self.config.RATE_LIMIT_DELAY)
        
        # Check with DeHashed if available
        if self.config_status['api_status'].get('dehashed') == 'configured':
            print("- Checking DeHashed...")
            results['sources']['dehashed'] = self.dehashed_client.check_password(password)
            time.sleep(self.config.RATE_LIMIT_DELAY)
        
        # Aggregate results
        results['summary'] = self._aggregate_password_results(results['sources'])
        
        return results
    
    def check_email(self, email: str) -> Dict:
        """
        Comprehensive email checking menggunakan multiple sources
        """
        results = {
            'email': email,
            'timestamp': time.time(),
            'sources': {}
        }
        
        print(f"Checking {email} with multiple sources...")
        
        # Check local database first (fastest)
        print("- Checking local database...")
        results['sources']['local'] = self.local_client.check_email(email)
        
        # Check DeHashed if configured
        if self.config_status['api_status'].get('dehashed') == 'configured':
            print("- Checking DeHashed...")
            results['sources']['dehashed'] = self.dehashed_client.check_email(email)
            time.sleep(self.config.RATE_LIMIT_DELAY)
        
        # Check HIBP (rate limited)
        print("- Checking HIBP...")
        results['sources']['hibp'] = self.hibp_client.check_email(email)
        time.sleep(self.config.RATE_LIMIT_DELAY)
        
        # Check Intelligence X if configured
        if self.config_status['api_status'].get('intelx') == 'configured':
            print("- Checking Intelligence X...")
            results['sources']['intelx'] = self.intelx_client.check_email(email)
            time.sleep(self.config.RATE_LIMIT_DELAY)
        
        # Aggregate results
        results['summary'] = self._aggregate_email_results(results['sources'])
        
        # Update statistics
        self._update_stats(results['summary']['found'])
        
        return results
    
    def comprehensive_check(self, email: str, password: str = None) -> Dict:
        """
        Complete breach check untuk email dan password
        """
        results = {
            'email': email,
            'timestamp': time.time(),
            'config_status': self.config_status
        }
        
        print(f"Starting comprehensive check for {email}...")
        
        # Check email
        email_results = self.check_email(email)
        results['email_check'] = email_results
        
        # Check password if provided
        if password:
            password_results = self.check_password(password)
            results['password_check'] = password_results
        
        # Overall summary
        results['overall_summary'] = self._create_overall_summary(results)
        
        return results
    
    def _aggregate_password_results(self, sources: Dict) -> Dict:
        """Aggregate password results from multiple sources"""
        summary = {
            'found': False,
            'total_breaches': 0,
            'sources_checked': len(sources),
            'sources_successful': 0,
            'sources_failed': 0,
            'highest_count': 0,
            'recommendations': []
        }
        
        for source_name, result in sources.items():
            if result.get('status') in ['found', 'success']:
                summary['sources_successful'] += 1
                if result.get('pwned') or result.get('found'):
                    summary['found'] = True
                    count = result.get('count', 0)
                    summary['total_breaches'] += count
                    if count > summary['highest_count']:
                        summary['highest_count'] = count
            else:
                summary['sources_failed'] += 1
        
        # Generate recommendations
        if summary['found']:
            summary['recommendations'] = [
                'Change this password immediately',
                'Enable two-factor authentication',
                'Use a unique password for each account',
                'Consider using a password manager'
            ]
        else:
            summary['recommendations'] = [
                'Password appears to be safe',
                'Continue using strong, unique passwords',
                'Regular security checkups recommended'
            ]
        
        return summary
    
    def _aggregate_email_results(self, sources: Dict) -> Dict:
        """Aggregate email results from multiple sources"""
        summary = {
            'found': False,
            'total_breaches': 0,
            'sources_checked': len(sources),
            'sources_successful': 0,
            'sources_failed': 0,
            'breach_sources': [],
            'recommendations': []
        }
        
        for source_name, result in sources.items():
            if result.get('status') in ['found', 'success', 'clean']:
                summary['sources_successful'] += 1
                if result.get('found'):
                    summary['found'] = True
                    summary['breach_sources'].append(source_name)
                    total = result.get('total', 1)
                    summary['total_breaches'] += total
            else:
                summary['sources_failed'] += 1
        
        # Generate recommendations
        if summary['found']:
            summary['recommendations'] = [
                'Your email was found in data breaches',
                'Change passwords for affected accounts',
                'Enable two-factor authentication',
                'Monitor accounts for suspicious activity',
                'Consider using email aliases for different services'
            ]
        else:
            summary['recommendations'] = [
                'Email not found in checked breach databases',
                'Continue monitoring for new breaches',
                'Use strong, unique passwords',
                'Enable security notifications'
            ]
        
        return summary
    
    def _create_overall_summary(self, results: Dict) -> Dict:
        """Create overall summary of all checks"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'email_status': 'unknown',
            'password_status': 'unknown',
            'risk_level': 'unknown',
            'action_required': False,
            'recommendations': []
        }
        
        # Email status
        if 'email_check' in results:
            email_summary = results['email_check']['summary']
            summary['email_status'] = 'breached' if email_summary['found'] else 'clean'
        
        # Password status
        if 'password_check' in results:
            password_summary = results['password_check']['summary']
            summary['password_status'] = 'breached' if password_summary['found'] else 'clean'
        
        # Risk assessment
        if summary['email_status'] == 'breached' and summary['password_status'] == 'breached':
            summary['risk_level'] = 'high'
            summary['action_required'] = True
        elif summary['email_status'] == 'breached' or summary['password_status'] == 'breached':
            summary['risk_level'] = 'medium'
            summary['action_required'] = True
        else:
            summary['risk_level'] = 'low'
        
        # Combine recommendations
        if 'email_check' in results:
            summary['recommendations'].extend(results['email_check']['summary']['recommendations'])
        if 'password_check' in results:
            summary['recommendations'].extend(results['password_check']['summary']['recommendations'])
        
        # Remove duplicates
        summary['recommendations'] = list(set(summary['recommendations']))
        
        return summary
    
    def _update_stats(self, breach_found: bool):
        """Update internal statistics"""
        self.stats['total_checks'] += 1
        self.stats['last_check'] = datetime.now().isoformat()
        
        if breach_found:
            self.stats['successful_checks'] += 1
        else:
            self.stats['failed_checks'] += 1
    
    def get_status(self) -> Dict:
        """Get current status of breach checker"""
        return {
            'config_status': self.config_status,
            'stats': self.stats,
            'available_sources': {
                'hibp': True,
                'dehashed': self.config_status['api_status'].get('dehashed') == 'configured',
                'intelx': self.config_status['api_status'].get('intelx') == 'configured',
                'local_db': self.config_status['api_status'].get('local_db') == 'available'
            }
        }
    
    def get_local_db_stats(self) -> Dict:
        """Get local database statistics"""
        return self.local_client.get_stats()

def main():
    """Test the refactored breach checker"""
    checker = BreachChecker()
    
    print("🔍 Refactored Breach Checker Test")
    print("=" * 50)
    
    # Show status
    status = checker.get_status()
    print("📊 System Status:")
    print(f"  Configuration valid: {status['config_status']['valid']}")
    print(f"  Available sources: {sum(status['available_sources'].values())}/4")
    
    # Test comprehensive check
    test_email = "test@example.com"
    test_password = "Password12345"
    
    print(f"\n🧪 Testing: {test_email}")
    print("-" * 30)
    
    results = checker.comprehensive_check(test_email, test_password)
    
    # Print summary
    print("\n📋 RESULTS SUMMARY:")
    overall = results['overall_summary']
    print(f"  Email Status: {overall['email_status']}")
    print(f"  Password Status: {overall['password_status']}")
    print(f"  Risk Level: {overall['risk_level']}")
    print(f"  Action Required: {overall['action_required']}")
    
    print("\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(overall['recommendations'][:5], 1):
        print(f"  {i}. {rec}")
    
    # Save detailed results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n💾 Detailed results saved to test_results.json")

if __name__ == "__main__":
    main()
