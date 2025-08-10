# Setup DeHashed API

Anda sudah memiliki API key DeHashed: `7AG14cikiWpWmLbU0TdsJXGEGE26r+1iAooR2/f7wgHHzItdVLUSPek=`

## 🔧 Cara Setup:

### 1. **Update Email DeHashed**
Edit file `breach_checker.py` line ~55:

```python
# Ganti dengan email yang Anda gunakan untuk daftar DeHashed
api_email = "your-registered-email@example.com"  # GANTI INI
```

### 2. **Uncomment Code**
Di file `breach_checker.py`, uncomment code yang ada di dalam triple quotes `"""` pada function `check_dehashed_free()`.

### 3. **Test API**
```bash
cd flask-app
source venv/bin/activate
python3 test_dehashed.py
```

## 📋 Status Saat Ini:

✅ **API Key**: Sudah tersedia  
⚠️ **Email**: Perlu diupdate dengan email DeHashed Anda  
⚠️ **Code**: Perlu di-uncomment setelah email diupdate  

## 🔍 Sumber Data yang Sudah Aktif:

✅ **HIBP Pwned Passwords** - 100% berfungsi, gratis  
✅ **Local Database** - Berfungsi dengan 10 test emails  
⚠️ **DeHashed** - Perlu setup email  
❌ **Intelligence X** - Perlu API key  

## 🚀 Cara Menggunakan Tanpa DeHashed:

Aplikasi sudah berfungsi dengan baik menggunakan:
1. **HIBP Pwned Passwords** untuk password checking
2. **Local Database** untuk email checking

```bash
cd flask-app
source venv/bin/activate
python app.py
```

Akses di: http://localhost:5000

## 📝 Catatan:

- DeHashed memerlukan email yang terdaftar untuk authentication
- API key sudah benar, hanya perlu email yang sesuai
- Tanpa DeHashed, aplikasi tetap berfungsi dengan sumber data lain
- Local database bisa ditambah dengan dataset breach lainnya
