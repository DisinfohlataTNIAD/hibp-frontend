# HIBP Frontend - BreachedCheck

Aplikasi web untuk checking data breach sebagai alternatif gratis Have I Been Pwned (HIBP).

## 🚀 Quick Start

```bash
# Masuk ke Flask app
cd flask-app

# Aktifkan virtual environment
source venv/bin/activate

# Jalankan aplikasi
python app.py
```

**Akses di: http://localhost:5000**

## 📁 Project Structure

```
hibp-frontend/
├── flask-app/              # Flask web application
│   ├── app.py             # Main Flask app
│   ├── breach_checker.py  # Core breach checking logic
│   ├── templates/         # HTML templates
│   ├── static/           # CSS, JS, Images
│   ├── venv/             # Python virtual environment
│   └── README.md         # Detailed Flask app docs
└── .git/                 # Git repository
```

## ✨ Features

- 🔍 **Email/Username Check** - Multi-source breach detection
- 🔐 **Password Check** - K-anonymity HIBP integration  
- 📱 **PWA Ready** - Installable, offline capable
- 🆓 **100% Free** - No API costs for basic features
- 🔒 **Privacy First** - No data stored on server
- 🌐 **Multiple Sources** - HIBP, DeHashed, Intelligence X, Local DB

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Frontend**: Vanilla JS, CSS
- **APIs**: HIBP Pwned Passwords, DeHashed, Intelligence X
- **Database**: Local file-based breach database

## 📖 Documentation

Lihat dokumentasi lengkap di: [`flask-app/README.md`](flask-app/README.md)

## 🔧 Development

```bash
cd flask-app
source venv/bin/activate
export FLASK_ENV=development
python app.py
```

## 🚀 Production

```bash
cd flask-app
source venv/bin/activate
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 License

Open source project - feel free to use and modify.

---

**Note**: Semua file aplikasi sekarang ada di folder `flask-app/`. File duplikat di root directory sudah dihapus untuk menjaga kebersihan project.
