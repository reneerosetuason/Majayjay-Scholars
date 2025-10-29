from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
#ehwjahdkjassdbfkajsb,madn
app = Flask(__name__)
app.secret_key = "ren02"

# ================== DATABASE CONNECTION ==================
db = mysql.connector.connect(
    host="localhost",
    user="root",          # change if needed
    password="ren123",    # your MySQL password
    database="usersdb"    # make sure this DB exists
)

# ================== ROUTES ==================

@app.route('/')
def home():
    if 'user_id' in session:
        user_type = session.get('user_type', '').lower()
        if user_type == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user_type == 'mayor':
            return redirect(url_for('mayor_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if not all([email, password, confirm]):
            flash("Please fill out all fields.", "error")
            return redirect(url_for('register'))

        if password != confirm:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))

        cursor = db.cursor()

        try:
            # Insert user with default name = email (since no name input)
            cursor.execute("""
                INSERT INTO users (name, email, password, user_type)
                VALUES (%s, %s, %s, %s)
            """, (email.split('@')[0], email, password, 'student'))
            db.commit()

            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('login'))  #Redirects to login after register

        except mysql.connector.IntegrityError:
            flash("Email already exists!", "error")

        finally:
            cursor.close()

    return render_template('register.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        # Simple password check (plain text)
        if user and user['password'] == password:
            session['user_id'] = user['user_id']
            session['email'] = user['email']
            session['user_type'] = user['user_type']

            flash("Login successful!", "success")

            role = user['user_type'].strip().lower()
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'mayor':
                return redirect(url_for('mayor_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid email or password.", "error")

    return render_template('login.html')

# ---------- ADMIN DASHBOARD ----------
@app.route('/admin')
def admin_dashboard():
    if session.get('user_type', '').lower() == 'admin':
        cursor = db.cursor(dictionary=True)

        # Fetch all users
        cursor.execute("SELECT user_id, name, email, user_type FROM users")
        users = cursor.fetchall()

        # Fetch logged-in admin info
        cursor.execute("SELECT name FROM users WHERE user_id = %s", (session['user_id'],))
        current_admin = cursor.fetchone()
        cursor.close()

        name = current_admin['name'] if current_admin and current_admin['name'] else session['email']
        return render_template('admin/admin_dashboard.html', users=users, name=name)

    flash("Access denied!", "error")
    return redirect(url_for('login'))

# ---------- MAYOR DASHBOARD ----------
@app.route('/mayor')
def mayor_dashboard():
    if session.get('user_type', '').lower() == 'mayor':
        return "Welcome, Mayor!"
    flash("Access denied!", "error")
    return redirect(url_for('login'))

# ---------- STUDENT DASHBOARD ----------
@app.route('/student')
def student_dashboard():
    if session.get('user_type', '').lower() == 'student':
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, user_type FROM users")
        users = cursor.fetchall()
        cursor.close()
        return render_template('student/student_dashboard.html', users=users)
    flash("Access denied!", "error")
    return redirect(url_for('login'))

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

# ================== MAIN ==================
if __name__ == '__main__':
    app.run(debug=True)
