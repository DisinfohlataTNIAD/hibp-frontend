#!/usr/bin/env python3
"""
Setup script untuk mendapatkan API keys gratis
"""

def print_api_setup_guide():
    """
    Guide untuk setup API keys gratis
    """
    print("=== SETUP API KEYS GRATIS ===\n")
    
    print("1. HIBP Pwned Passwords API")
    print("   ✅ GRATIS - Tidak perlu API key")
    print("   📝 Sudah terintegrasi dalam script")
    print("   🔗 https://haveibeenpwned.com/API/v3#PwnedPasswords\n")
    
    print("2. DeHashed API (Free Tier)")
    print("   📧 Daftar: https://dehashed.com/")
    print("   💰 Free tier: 100 queries/bulan")
    print("   📝 Setelah daftar, dapatkan API key dari dashboard")
    print("   🔧 Update variable 'api_key' di breach_checker.py\n")
    
    print("3. Intelligence X API")
    print("   📧 Daftar: https://intelx.io/")
    print("   💰 Free tier: Limited queries")
    print("   📝 Dapatkan API key setelah verifikasi email")
    print("   🔧 Update variable 'api_key' di breach_checker.py\n")
    
    print("4. Database Breach Lokal")
    print("   📁 Download dataset breach dari:")
    print("   - https://github.com/danielmiessler/SecLists")
    print("   - https://weakpass.com/")
    print("   - Public breach datasets")
    print("   📝 Simpan email dalam file 'local_breaches.txt'\n")
    
    print("=== ALTERNATIF SUMBER DATA GRATIS ===\n")
    
    print("🔍 Sumber Dataset Breach Gratis:")
    print("   • Collection #1-5 (Archive.org)")
    print("   • Exploit.in forums")
    print("   • GitHub leaked credentials")
    print("   • Pastebin dumps")
    print("   • Troy Hunt's sample data\n")
    
    print("🛠️  Tools untuk Scraping (Hati-hati ToS):")
    print("   • BeautifulSoup untuk web scraping")
    print("   • Selenium untuk dynamic content")
    print("   • Scrapy untuk large scale scraping\n")
    
    print("⚠️  PERINGATAN:")
    print("   • Selalu respect rate limits")
    print("   • Baca Terms of Service")
    print("   • Jangan abuse free tiers")
    print("   • Consider privacy implications")

def create_config_template():
    """
    Buat template config file
    """
    config_content = """# Configuration file untuk Breach Checker
# Ganti dengan API keys Anda

[API_KEYS]
dehashed_api_key = YOUR_DEHASHED_API_KEY
intelx_api_key = YOUR_INTELX_API_KEY

[SETTINGS]
rate_limit_delay = 1
max_retries = 3
timeout = 30

[LOCAL_DB]
breach_file = local_breaches.txt
update_interval = 86400  # 24 hours in seconds
"""
    
    with open('config.ini', 'w') as f:
        f.write(config_content)
    
    print("✅ Template config.ini dibuat!")
    print("📝 Edit file config.ini dengan API keys Anda")

if __name__ == "__main__":
    print_api_setup_guide()
    print("\n" + "="*50)
    create_config_template()
