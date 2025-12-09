# Quick Start Guide - Supabase Migration

## 🚀 Get Started in 5 Minutes

### 1. Create Database Tables (2 minutes)

1. Go to: https://supabase.com/dashboard/project/lsafdwxgrstukbcfohbw/editor
2. Click **SQL Editor** → **New Query**
3. Open `database/supabase_schema.sql` file
4. Copy all content and paste into SQL Editor
5. Click **Run** ▶️

### 2. Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### 3. Backup Current App (30 seconds)

```bash
copy app.py app_mysql_backup.py
```

### 4. Switch to Supabase (30 seconds)

```bash
copy app_supabase.py app.py
```

### 5. Run Application (30 seconds)

```bash
python app.py
```

### 6. Test It! (1 minute)

Open browser: http://localhost:5000

Try:
- Register a new account
- Login
- Submit an application

## ✅ Done!

Your app now uses Supabase instead of MySQL!

## 🔙 Rollback (if needed)

```bash
copy app_mysql_backup.py app.py
python app.py
```

## 📋 Files Created

- `.env` - Your credentials (DO NOT SHARE)
- `requirements.txt` - Python dependencies
- `app_supabase.py` - New app with Supabase
- `database/supabase_schema.sql` - Database schema
- `.gitignore` - Protects sensitive files
- `MIGRATION_GUIDE.md` - Detailed instructions
- `QUICK_START.md` - This file

## 🆘 Having Issues?

Check `MIGRATION_GUIDE.md` for detailed troubleshooting.

## 🎉 Benefits

✅ No local database needed
✅ Cloud-based (access anywhere)
✅ Automatic backups
✅ Free tier included
✅ Scales automatically
✅ Same functionality, better infrastructure
