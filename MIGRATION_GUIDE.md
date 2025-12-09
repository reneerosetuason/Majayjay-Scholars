# Migration Guide: MySQL to Supabase

## ✅ What Has Been Done

1. **Created `.env` file** - Stores all sensitive credentials securely
2. **Created `requirements.txt`** - Lists all Python dependencies including Supabase
3. **Created `app_supabase.py`** - New Flask app using Supabase instead of MySQL
4. **Created `supabase_schema.sql`** - PostgreSQL schema for Supabase database
5. **Created `.gitignore`** - Protects credentials from being committed to Git

## 📋 Migration Steps

### Step 1: Set Up Supabase Database

1. Go to your Supabase dashboard: https://supabase.com/dashboard/project/lsafdwxgrstukbcfohbw
2. Click on **SQL Editor** in the left sidebar
3. Click **New Query**
4. Copy the entire content from `database/supabase_schema.sql`
5. Paste it into the SQL Editor
6. Click **Run** to create all tables

### Step 2: Install Dependencies

Open your terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask
- Supabase Python client
- python-dotenv
- Werkzeug

### Step 3: Migrate Existing Data (Optional)

If you have existing data in MySQL that you want to migrate:

1. Export data from MySQL:
```bash
mysqldump -u root -p usersdb > backup.sql
```

2. Convert MySQL data to PostgreSQL format (you may need to manually adjust)
3. Import to Supabase using the SQL Editor

**OR** start fresh with an empty database (recommended for testing)

### Step 4: Test the New Application

1. **Backup your current app.py:**
```bash
copy app.py app_mysql_backup.py
```

2. **Replace app.py with the new Supabase version:**
```bash
copy app_supabase.py app.py
```

3. **Run the application:**
```bash
python app.py
```

4. **Test all features:**
   - ✅ Registration with email verification
   - ✅ Login
   - ✅ Student dashboard
   - ✅ Apply for scholarship
   - ✅ Renew scholarship
   - ✅ View applications
   - ✅ Edit applications
   - ✅ Admin dashboard
   - ✅ Mayor dashboard

### Step 5: Verify Everything Works

Test each user type:
- **Student**: Register, login, apply, renew, view applications
- **Admin**: Login, view all users
- **Mayor**: Login, view applications and renewals

## 🔑 Key Changes

### Database Connection
**Before (MySQL):**
```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ren123",
    database="usersdb"
)
```

**After (Supabase):**
```python
from supabase import create_client
supabase = create_client(supabase_url, supabase_key)
```

### Query Syntax
**Before (MySQL):**
```python
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
user = cursor.fetchone()
```

**After (Supabase):**
```python
response = supabase.table('users').select('*').eq('email', email).execute()
user = response.data[0] if response.data else None
```

### Insert Operations
**Before (MySQL):**
```python
cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
db.commit()
```

**After (Supabase):**
```python
supabase.table('users').insert({'email': email, 'password': password}).execute()
```

### Update Operations
**Before (MySQL):**
```python
cursor.execute("UPDATE application SET status = %s WHERE application_id = %s", (status, app_id))
db.commit()
```

**After (Supabase):**
```python
supabase.table('application').update({'status': status}).eq('application_id', app_id).execute()
```

## 🔒 Security Notes

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use `.gitignore`** - Already created to protect sensitive files
3. **Environment variables** - All credentials are now in `.env` file
4. **Password hashing** - Consider adding password hashing (bcrypt) in production

## 🚀 Benefits of Supabase

1. **No local database** - Everything is in the cloud
2. **Automatic backups** - Supabase handles backups
3. **Real-time capabilities** - Can add real-time features later
4. **Built-in authentication** - Can use Supabase Auth in future
5. **Scalability** - Automatically scales with your needs
6. **Free tier** - Generous free tier for development

## 📊 Database Schema Differences

### MySQL → PostgreSQL Changes:
- `AUTO_INCREMENT` → `SERIAL`
- `ENUM('value1', 'value2')` → Custom ENUM types
- `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` → Trigger function
- No `USE database;` statement needed

## 🐛 Troubleshooting

### Issue: "Module not found: supabase"
**Solution:** Run `pip install -r requirements.txt`

### Issue: "Connection refused"
**Solution:** Check your `.env` file has correct SUPABASE_URL and SUPABASE_KEY

### Issue: "Table does not exist"
**Solution:** Run the `supabase_schema.sql` in Supabase SQL Editor

### Issue: "Authentication failed"
**Solution:** Verify your Supabase API key in `.env` file

## 📝 Next Steps (Optional Improvements)

1. **Add password hashing:**
```python
from werkzeug.security import generate_password_hash, check_password_hash
```

2. **Use Supabase Storage** for file uploads instead of local storage

3. **Enable Row Level Security (RLS)** in Supabase for better security

4. **Add Supabase Auth** to replace custom authentication

5. **Set up automatic backups** in Supabase dashboard

## 🎯 Rollback Plan

If something goes wrong:

1. Stop the application
2. Restore original app.py:
```bash
copy app_mysql_backup.py app.py
```
3. Your MySQL database is unchanged
4. Restart with original setup

## ✨ Success Checklist

- [ ] Supabase tables created successfully
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Application starts without errors
- [ ] Can register new user
- [ ] Can login
- [ ] Can submit application
- [ ] Can view applications
- [ ] Admin dashboard works
- [ ] Mayor dashboard works

## 📞 Support

If you encounter issues:
1. Check the console for error messages
2. Verify Supabase dashboard shows your tables
3. Confirm `.env` file has correct credentials
4. Check Supabase logs in dashboard

---

**Migration completed! Your application now uses Supabase (PostgreSQL) instead of MySQL Workbench.**
