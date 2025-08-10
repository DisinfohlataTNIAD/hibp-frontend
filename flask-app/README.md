# BreachedCheck Flask App

Aplikasi web Flask untuk checking data breach menggunakan UI yang sudah ada dengan backend Python.

## Features

✅ **UI yang sudah ada** - Menggunakan frontend BreachedCheck yang sudah dibuat  
✅ **Backend Python** - Flask API dengan breach checker gratis  
✅ **Multiple Sources** - HIBP, DeHashed, Intelligence X, Local DB  
✅ **K-Anonymity** - Password checking yang aman  
✅ **PWA Ready** - Service worker dan manifest sudah ada  

## Quick Start

```bash
# 1. Masuk ke directory flask-app
cd flask-app

# 2. Aktifkan virtual environment
source venv/bin/activate

# 3. Install dependencies (sudah terinstall)
pip install flask requests

# 4. Jalankan aplikasi
python app.py
```

Akses di: **http://localhost:5000**

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/check-account` | Check email/username breach |
| POST | `/api/check-password` | Check password menggunakan k-anonymity |
| POST | `/api/notify` | Subscribe notification |
| GET | `/api/breaches` | List semua breaches |
| GET | `/api/stats` | Statistik aplikasi |

## File Structure

```
flask-app/
├── app.py                 # Flask application
├── breach_checker.py      # Core breach checking logic
├── templates/             # HTML templates
│   ├── index.html        # Homepage
│   ├── breaches.html     # Breaches list
│   ├── breach.html       # Single breach
│   └── stats.html        # Statistics
├── static/               # Static files
│   ├── assets/          # CSS, JS, Images
│   ├── manifest.webmanifest
│   └── sw.js            # Service worker
└── venv/                # Virtual environment
```

## Setup API Keys (Opsional)

Untuk menggunakan sumber data tambahan:

1. **DeHashed API** (100 queries/bulan gratis)
   - Daftar: https://dehashed.com/
   - Edit `breach_checker.py` line ~45

2. **Intelligence X API** (limited queries gratis)  
   - Daftar: https://intelx.io/
   - Edit `breach_checker.py` line ~75

3. **Local Database**
   - Tambah email ke `local_breaches.txt`
   - Download dataset dari SecLists, WeakPass, dll

## Yang Sudah Berfungsi

✅ **HIBP Pwned Passwords** - 100% gratis, no API key  
✅ **Local Database** - Cepat dan customizable  
✅ **Frontend Integration** - UI existing terintegrasi  
✅ **PWA Features** - Offline capable  

## Development

```bash
# Run in development mode
export FLASK_ENV=development
python app.py

# Test API endpoints
curl -X POST http://localhost:5000/api/check-account \
  -H "Content-Type: application/json" \
  -d '{"account":"test@example.com"}'

curl -X POST http://localhost:5000/api/check-password \
  -H "Content-Type: application/json" \
  -d '{"password":"password123"}'
```

## Production Deployment

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Security Notes

- Password checking menggunakan k-anonymity (aman)
- Data tidak disimpan di server
- HTTPS recommended untuk production
- Rate limiting diimplementasi
- Input validation pada semua endpoints

## Troubleshooting

**Error: Module not found**
```bash
# Pastikan virtual environment aktif
source venv/bin/activate
```

**API Key errors**
```bash
# Edit breach_checker.py dan ganti placeholder API keys
# Atau gunakan hanya local database + HIBP passwords
```

**CORS issues**
```bash
# Install flask-cors jika diperlukan
pip install flask-cors
```
