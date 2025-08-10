#!/usr/bin/env python3
"""
Flask Application untuk Breach Checker
Clean architecture dengan separation of concerns
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os
import time
from datetime import datetime

# Import refactored components
from config import get_config, validate_config
from breach_checker import BreachChecker

# Get configuration
config_class = get_config()
app = Flask(__name__)
app.config.from_object(config_class)

# Initialize breach checker
checker = BreachChecker()

@app.route('/')
def index():
    """Homepage - render existing index.html"""
    return render_template('index.html')

@app.route('/breaches.html')
def breaches():
    """Breaches page"""
    return render_template('breaches.html')

@app.route('/breach.html')
def breach():
    """Single breach page"""
    return render_template('breach.html')

@app.route('/stats.html')
def stats():
    """Stats page"""
    return render_template('stats.html')

# API Endpoints

@app.route('/api/check-account', methods=['POST'])
def api_check_account():
    """API endpoint untuk check email/username"""
    try:
        data = request.get_json()
        account = data.get('account', '').strip()
        
        if not account:
            return jsonify({'error': 'Account tidak boleh kosong'}), 400
        
        # Check menggunakan refactored breach checker
        results = checker.check_email(account)
        
        # Format response untuk frontend compatibility
        response = {
            'found': results['summary']['found'],
            'breaches': [],
            'sources': results['sources'],
            'summary': results['summary'],
            'timestamp': results['timestamp']
        }
        
        # Extract breach details
        for source_name, source_result in results['sources'].items():
            if source_result.get('found'):
                response['breaches'].append({
                    'source': source_name,
                    'data': source_result
                })
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-password', methods=['POST'])
def api_check_password():
    """API endpoint untuk check password menggunakan k-anonymity"""
    try:
        data = request.get_json()
        password = data.get('password', '').strip()
        
        if not password:
            return jsonify({'error': 'Password tidak boleh kosong'}), 400
        
        # Check password menggunakan refactored checker
        results = checker.check_password(password)
        
        # Format response untuk frontend compatibility
        hibp_result = results['sources'].get('hibp', {})
        response = {
            'pwned': hibp_result.get('pwned', False),
            'count': hibp_result.get('count', 0),
            'message': hibp_result.get('message', 'Password check completed'),
            'sources': results['sources'],
            'summary': results['summary'],
            'timestamp': results['timestamp']
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comprehensive-check', methods=['POST'])
def api_comprehensive_check():
    """API endpoint untuk comprehensive check (email + password)"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email:
            return jsonify({'error': 'Email tidak boleh kosong'}), 400
        
        # Comprehensive check
        results = checker.comprehensive_check(email, password if password else None)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notify', methods=['POST'])
def api_notify():
    """API endpoint untuk notification subscription"""
    try:
        data = request.get_json()
        target = data.get('target', '').strip()
        contact = data.get('contact', '').strip()
        
        if not target:
            return jsonify({'error': 'Target tidak boleh kosong'}), 400
        
        # For now, just return success (implement notification system later)
        return jsonify({
            'success': True,
            'message': f'Subscription untuk "{target}" berhasil ditambahkan',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    """API endpoint untuk system status"""
    try:
        status = checker.get_status()
        
        # Add system info
        status['system'] = {
            'app_version': '2.0.0',
            'python_version': sys.version,
            'flask_debug': app.debug,
            'uptime': time.time() - app.start_time if hasattr(app, 'start_time') else 0
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sources')
def api_sources():
    """API untuk mendapatkan status sumber data"""
    try:
        config_status = validate_config()
        
        sources_status = {
            'hibp_passwords': {
                'name': 'HIBP Pwned Passwords',
                'status': 'active',
                'free': True,
                'description': 'Check password breaches menggunakan k-anonymity',
                'reliability': 'high'
            },
            'local_db': {
                'name': 'Local Database',
                'status': config_status['api_status'].get('local_db', 'unknown'),
                'free': True,
                'description': 'Database breach lokal',
                'reliability': 'high'
            },
            'hibp_api': {
                'name': 'HIBP Breached Accounts',
                'status': 'limited',
                'free': True,
                'description': 'Rate limited, requires API key for full access',
                'reliability': 'medium'
            },
            'dehashed': {
                'name': 'DeHashed API v2',
                'status': config_status['api_status'].get('dehashed', 'unknown'),
                'free': True,
                'description': 'Password search working, email search requires subscription',
                'reliability': 'medium'
            },
            'intelx': {
                'name': 'Intelligence X',
                'status': config_status['api_status'].get('intelx', 'unknown'),
                'free': True,
                'description': 'Limited queries gratis',
                'reliability': 'unknown'
            }
        }
        
        return jsonify(sources_status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/breaches')
def api_breaches():
    """API endpoint untuk mendapatkan daftar breaches"""
    # Sample data - implement with real breach database later
    breaches = [
        {
            'name': 'LinkedIn',
            'date': '2012-06-05',
            'accounts': 164000000,
            'description': 'Professional networking platform breach',
            'verified': True
        },
        {
            'name': 'Yahoo',
            'date': '2013-08-01',
            'accounts': 3000000000,
            'description': 'Massive email service breach',
            'verified': True
        },
        {
            'name': 'Facebook',
            'date': '2019-04-01',
            'accounts': 533000000,
            'description': 'Social media platform data exposure',
            'verified': True
        }
    ]
    
    return jsonify(breaches)

@app.route('/api/stats')
def api_stats():
    """API endpoint untuk statistik aplikasi"""
    try:
        # Get system stats
        system_stats = checker.get_status()
        
        # Get local database stats
        local_stats = checker.get_local_db_stats()
        
        stats = {
            'system': system_stats,
            'local_database': local_stats,
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Static file serving
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve static assets"""
    return send_from_directory('static/assets', filename)

@app.route('/manifest.webmanifest')
def manifest():
    """Serve PWA manifest"""
    return send_from_directory('static', 'manifest.webmanifest')

@app.route('/sw.js')
def service_worker():
    """Serve service worker"""
    return send_from_directory('static', 'sw.js')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint tidak ditemukan'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def rate_limit_error(error):
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

# Application startup
def create_app(config_name=None):
    """Application factory"""
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Set start time for uptime calculation
    app.start_time = time.time()
    
    return app

if __name__ == '__main__':
    # Validate configuration on startup
    config_status = validate_config()
    
    print("🚀 Starting BreachedCheck Flask App...")
    print("=" * 50)
    print(f"📱 Access at: http://localhost:{app.config['PORT']}")
    print(f"🔧 Debug mode: {app.config['DEBUG']}")
    print(f"⚙️  Configuration valid: {config_status['valid']}")
    
    if config_status['warnings']:
        print("⚠️  Warnings:")
        for warning in config_status['warnings']:
            print(f"   - {warning}")
    
    print("\n🔍 Available API endpoints:")
    endpoints = [
        "POST /api/check-account",
        "POST /api/check-password", 
        "POST /api/comprehensive-check",
        "POST /api/notify",
        "GET /api/status",
        "GET /api/sources",
        "GET /api/breaches",
        "GET /api/stats"
    ]
    for endpoint in endpoints:
        print(f"   - {endpoint}")
    
    print("\n" + "=" * 50)
    
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
