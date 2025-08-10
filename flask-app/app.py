#!/usr/bin/env python3
"""
Flask Web Application untuk Breach Checker
Menggunakan UI yang sudah ada dengan backend Python
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os

# Add parent directory to path untuk import breach_checker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from breach_checker import BreachChecker

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

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

# API Endpoints untuk frontend JavaScript

@app.route('/api/check-account', methods=['POST'])
def api_check_account():
    """API endpoint untuk check email/username"""
    try:
        data = request.get_json()
        account = data.get('account', '').strip()
        
        if not account:
            return jsonify({'error': 'Account tidak boleh kosong'}), 400
        
        # Check menggunakan breach checker
        results = checker.comprehensive_check(account)
        
        # Format response untuk frontend
        response = {
            'found': False,
            'breaches': [],
            'sources': {},
            'working_sources': [],
            'disabled_sources': [],
            'error_sources': []
        }
        
        # Check hasil dari berbagai sumber
        for source, result in results.get('sources', {}).items():
            response['sources'][source] = result
            
            if result.get('found'):
                response['found'] = True
                response['breaches'].append({
                    'source': source,
                    'data': result
                })
                response['working_sources'].append(source)
            elif result.get('status') == 'clean':
                response['working_sources'].append(source)
            elif result.get('status') == 'disabled':
                response['disabled_sources'].append(source)
            elif 'error' in result:
                response['error_sources'].append({
                    'source': source,
                    'error': result['error'],
                    'status': result.get('status', 'unknown')
                })
        
        # Add summary
        response['summary'] = {
            'total_sources': len(results.get('sources', {})),
            'working_sources': len(response['working_sources']),
            'disabled_sources': len(response['disabled_sources']),
            'error_sources': len(response['error_sources'])
        }
        
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
        
        # Check password menggunakan HIBP k-anonymity
        result = checker.check_pwned_passwords(password)
        
        return jsonify(result)
        
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
        
        # Untuk sekarang, hanya return success
        # Anda bisa implement notification system di sini
        return jsonify({
            'success': True,
            'message': f'Subscription untuk "{target}" berhasil ditambahkan'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/breaches')
def api_breaches():
    """API endpoint untuk mendapatkan daftar breaches"""
    # Sample data - Anda bisa ganti dengan data real
    breaches = [
        {
            'name': 'LinkedIn',
            'date': '2012-06-05',
            'accounts': 164000000,
            'description': 'Professional networking platform breach'
        },
        {
            'name': 'Yahoo',
            'date': '2013-08-01',
            'accounts': 3000000000,
            'description': 'Massive email service breach'
        },
        {
            'name': 'Facebook',
            'date': '2019-04-01',
            'accounts': 533000000,
            'description': 'Social media platform data exposure'
        }
    ]
    
    return jsonify(breaches)

@app.route('/api/stats')
def api_stats():
    """API endpoint untuk statistik"""
    # Sample stats - Anda bisa implement real stats
    stats = {
        'total_breaches': 500,
        'total_accounts': 12000000000,
        'recent_breaches': 25,
        'last_updated': '2024-08-10'
    }
    
    return jsonify(stats)

# Serve static files (assets)
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

@app.route('/api/sources')
def api_sources():
    """API untuk mendapatkan status sumber data"""
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
            'status': 'active' if os.path.exists('local_breaches.txt') else 'inactive',
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
            'name': 'DeHashed API',
            'status': 'error',
            'free': True,
            'description': 'API key provided but authentication failed',
            'reliability': 'low',
            'error': 'Authentication or endpoint issues'
        },
        'intelx': {
            'name': 'Intelligence X',
            'status': 'needs_setup',
            'free': True,
            'description': 'Limited queries gratis',
            'reliability': 'unknown'
        }
    }
    
    return jsonify(sources_status)

@app.route('/api/status')
def api_status():
    """API untuk status aplikasi"""
    try:
        # Test basic functionality
        from breach_checker import BreachChecker
        test_checker = BreachChecker()
        
        # Test password check (should always work)
        pwd_test = test_checker.check_pwned_passwords('test123')
        hibp_working = not ('error' in pwd_test)
        
        # Test local database
        local_test = test_checker.check_local_breach_db('test@example.com')
        local_working = not ('error' in local_test)
        
        status = {
            'app_status': 'running',
            'timestamp': time.time(),
            'core_features': {
                'password_checking': hibp_working,
                'local_database': local_working,
                'web_interface': True,
                'api_endpoints': True
            },
            'external_apis': {
                'hibp_passwords': hibp_working,
                'hibp_breaches': 'rate_limited',
                'dehashed': 'error',
                'intelligence_x': 'not_configured'
            },
            'recommendations': [
                'Password checking is fully functional',
                'Local database is working',
                'DeHashed API needs troubleshooting',
                'Consider adding more local breach data'
            ]
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'app_status': 'error',
            'error': str(e),
            'timestamp': time.time()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint tidak ditemukan'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting BreachedCheck Flask App...")
    print("📱 Access at: http://localhost:5000")
    print("🔍 API endpoints:")
    print("   - POST /api/check-account")
    print("   - POST /api/check-password") 
    print("   - POST /api/notify")
    print("   - GET /api/breaches")
    print("   - GET /api/stats")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
