from flask import Flask, render_template, request, redirect, flash, url_for, session
import os
from werkzeug.utils import secure_filename
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ren02"

# ================== FILE UPLOAD SETTINGS ==================
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ================== DATABASE CONNECTION ==================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ren123",
    database="usersdb"
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
            cursor.execute("""
                INSERT INTO users (name, email, password, user_type)
                VALUES (%s, %s, %s, %s)
            """, (email.split('@')[0], email, password, 'student'))
            db.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('login'))
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
        cursor.execute("SELECT user_id, name, email, user_type FROM users")
        users = cursor.fetchall()

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
        return render_template('student/student_dashboard.html')
    flash("Access denied!", "error")
    return redirect(url_for('login'))


# ---------- APPLY (NEW SCHOLARSHIP) ----------
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if session.get('user_type', '').lower() != 'student':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        student_id = request.form.get('student_id')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')
        course = request.form.get('course')
        year_level = request.form.get('year_level')
        gwa = request.form.get('gwa')
        reason = request.form.get('reason')

        # Handle files
        uploaded_files = {}
        for field in ['school_id', 'id_picture', 'birth_certificate', 'grades']:
            file = request.files.get(field)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files[field] = filename
            else:
                uploaded_files[field] = None

        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO application (
                    user_id, full_name, student_id, contact_number, address, 
                    course, year_level, gwa, reason, 
                    school_id, id_picture, birth_certificate, grades, 
                    status, submission_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending', CURRENT_TIMESTAMP)
            """, (
                session['user_id'], full_name, student_id, contact_number, address,
                course, year_level, gwa, reason,
                uploaded_files['school_id'], uploaded_files['id_picture'],
                uploaded_files['birth_certificate'], uploaded_files['grades']
            ))
            db.commit()
            flash("Application submitted successfully!", "success")
            return redirect(url_for('student_dashboard'))
        except Exception as e:
            print("Error inserting application:", e)
            flash("An error occurred while submitting your application.", "error")
        finally:
            cursor.close()

    return render_template('student/apply.html')


# ---------- RENEW SCHOLARSHIP ----------
@app.route('/renew_scholarship', methods=['GET', 'POST'])
def renew_scholarship():
    if session.get('user_type', '').lower() != 'student':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            user_id = session.get('user_id')

            full_name = request.form.get('full_name')
            student_id = request.form.get('student_id')
            contact_number = request.form.get('contact_number')
            address = request.form.get('address')
            course = request.form.get('course')
            year_level = request.form.get('year_level')
            gwa = request.form.get('gwa')
            reason = request.form.get('reason')

            uploaded_files = {}
            for field in ['school_id', 'id_picture', 'birth_certificate', 'grades']:
                file = request.files.get(field)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    uploaded_files[field] = filename
                else:
                    uploaded_files[field] = None

            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO application (
                    user_id, full_name, student_id, contact_number, address,
                    course, year_level, gwa, reason,
                    school_id, id_picture, birth_certificate, grades,
                    status, submission_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending', NOW())
            """, (
                user_id, full_name, student_id, contact_number, address,
                course, year_level, gwa, reason,
                uploaded_files['school_id'], uploaded_files['id_picture'],
                uploaded_files['birth_certificate'], uploaded_files['grades']
            ))

            db.commit()
            cursor.close()
            flash("✅ Renewal application submitted successfully!", "success")
            return redirect(url_for('student_dashboard'))

        except Exception as e:
            print("Error submitting renewal application:", e)
            flash("❌ Error submitting renewal application. Please try again.", "error")
            return redirect(url_for('renew_scholarship'))

    return render_template('student/renew_scholarship.html')


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


# ================== MAIN ==================
if __name__ == '__main__':
    app.run(debug=True)
