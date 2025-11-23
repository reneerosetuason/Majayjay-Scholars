from flask import Flask, render_template, request, jsonify, redirect, flash, url_for, session
import os
from werkzeug.utils import secure_filename
import mysql.connector
from datetime import datetime, timedelta
# ==================== EMAIL VERIFICATION SETUP ====================
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

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

# ==================== EMAIL VERIFICATION SETUP ====================
# Verification storage
verification_store = {}

# Email credentials
SENDER_EMAIL = "majayjayscholars@gmail.com"
SENDER_APP_PASSWORD = "zsxp iqvn klmd xqfw"

# ==================== HELPER FUNCTIONS ====================

def generate_verification_key(email):
    """Generate unique key for storing verification data"""
    return f"verify_{email}"

def store_verification_code(email, code):
    """Store verification code server-side with expiry"""
    key = generate_verification_key(email)
    verification_store[key] = {
        'email': email,
        'code': str(code),
        'verified': False,
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(minutes=10)
    }
    print(f"\n{'='*60}")
    print(f"[DEBUG] ✓ VERIFICATION CODE STORED FOR {email}")
    print(f"[DEBUG] Code: {code}")
    print(f"[DEBUG] Expires at: {verification_store[key]['expires_at']}")
    print(f"{'='*60}\n")

def get_verification_data(email):
    """Retrieve verification data"""
    key = generate_verification_key(email)
    data = verification_store.get(key)
    
    if data and datetime.now() > data['expires_at']:
        print(f"[DEBUG] Verification code for {email} has expired")
        del verification_store[key]
        return None
    
    return data

def verify_code_check(email, code):
    """Verify the code and mark as verified"""
    data = get_verification_data(email)
    
    if not data:
        print(f"[DEBUG] ❌ No verification data found for {email}")
        return False, "No verification code found. Please request a code first."
    
    stored_code = str(data['code']).strip()
    received_code = str(code).strip()
    
    print(f"\n[DEBUG] Code verification attempt:")
    print(f"  Email:    {email}")
    print(f"  Stored:   '{stored_code}'")
    print(f"  Received: '{received_code}'")
    print(f"  Match:    {stored_code == received_code}\n")
    
    if stored_code != received_code:
        print(f"[DEBUG] ❌ Code mismatch!")
        return False, "Incorrect verification code."
    
    # Mark as verified
    data['verified'] = True
    print(f"[DEBUG] ✓ Email {email} verified successfully")
    return True, "Email verified successfully."

def is_email_verified(email):
    """Check if email has been verified"""
    data = get_verification_data(email)
    return data and data['verified']

def cleanup_verification(email):
    """Clean up verification data after use"""
    key = generate_verification_key(email)
    if key in verification_store:
        del verification_store[key]
        print(f"[DEBUG] ✓ Cleaned up verification data for {email}")


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


# ==================== SEND CODE ROUTE ====================
@app.route('/send-code', methods=['POST'])
def send_code():
    try:
        data = request.get_json()
        email = data.get('email')

        print(f"\n{'='*60}")
        print(f"[DEBUG] SEND CODE REQUEST")
        print(f"[DEBUG] Email: {email}")
        print(f"{'='*60}\n")

        if not email:
            print("[DEBUG] ❌ No email provided")
            return jsonify({'status': 'error', 'message': 'Email is required'}), 400

        # Generate 6-digit code
        code = f"{random.randint(100000, 999999)}"
        print(f"[DEBUG] Generated code: {code}")

        # Store server-side
        store_verification_code(email, code)

        # Create email
        msg = MIMEMultipart('related')
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = "Your Verification Code - Majayjay Scholars Registration"

        # Alternative container
        alt = MIMEMultipart('alternative')
        msg.attach(alt)

        # HTML Email
        html = f"""
        <html>
          <body style="margin:0; padding:0; background:#ffffff;
          font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">

            <table width="100%" cellspacing="0" cellpadding="0" style="padding:40px 20px; text-align:center;">
              <tr><td>

                <div style="background: linear-gradient(135deg, #7a5af5 0%, #6745d1 100%); 
                            padding: 30px; border-radius: 15px; margin-bottom: 30px;">
                  <h1 style="margin:0; font-size:32px; font-weight:700; color:#fff;">
                    Majayjay Scholars
                  </h1>
                </div>

                <h2 style="margin:0 0 20px; font-size:24px; font-weight:600; color:#333;">
                  Email Verification
                </h2>

                <p style="margin:16px 0 30px; font-size:16px; color:#666;">
                  Enter this verification code to complete your registration
                </p>

                <table cellspacing="0" cellpadding="0" style="margin:0 auto;">
                  <tr>
                    <td style="background: linear-gradient(135deg, #7a5af5 0%, #6745d1 100%); 
                                padding:18px 40px; border-radius:10px; box-shadow: 0 4px 15px rgba(122, 90, 245, 0.3);">
                      <span style="font-size:28px; font-weight:700; color:#fff; letter-spacing:6px;">
                        {code}
                      </span>
                    </td>
                  </tr>
                </table>

                <p style="margin:30px 0 10px; font-size:14px; color:#999;">
                  ⏱️ This code expires in 10 minutes
                </p>
                
                <p style="margin:10px 0; font-size:14px; color:#999;">
                  If you didn't request this code, please ignore this email.
                </p>

                <div style="margin-top:40px; padding-top:30px; border-top:1px solid #eee;">
                  <p style="margin:0; font-size:12px; color:#999;">
                    © 2025 Majayjay Scholars Program. All rights reserved.
                  </p>
                </div>

              </td></tr>
            </table>

          </body>
        </html>
        """

        alt.attach(MIMEText(html, 'html'))

        # Send Email
        try:
            print(f"[DEBUG] Connecting to SMTP server...")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
                smtp.send_message(msg)
            print(f"[DEBUG] ✓ Email sent successfully to {email}")
        except Exception as e:
            print(f"[DEBUG] ❌ SMTP error: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to send email. Please check the email address.'}), 500

        return jsonify({'status': 'success', 'message': 'Verification code sent to email'}), 200

    except Exception as e:
        print(f"[DEBUG] ❌ Send code error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': 'Failed to send code'}), 500


# ==================== VERIFY CODE ROUTE ====================
@app.route('/verify-code', methods=['POST'])
def verify_code_endpoint():
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')

        print(f"\n[DEBUG] Verify attempt - Email: {email}, Code: {code}\n")

        if not email or not code:
            return jsonify({'status': 'failed', 'message': 'Email and code required'}), 400

        success, message = verify_code_check(email, code)
        
        if not success:
            return jsonify({'status': 'failed', 'message': message}), 400

        return jsonify({'status': 'success', 'message': 'Email verified successfully'}), 200

    except Exception as e:
        print(f"[DEBUG] ❌ Verify code error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'failed', 'message': 'Server error during verification'}), 500


# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        email_verified = request.form.get('email_verified')

        if not all([email, password, confirm]):
            flash("Please fill out all fields.", "error")
            return redirect(url_for('register'))

        # Check if email is verified
        if email_verified != 'true' or not is_email_verified(email):
            flash('Please verify your email before registering', 'error')
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
            
            # Clean up verification data after successful registration
            cleanup_verification(email)
            
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


# ---------- MAYOR DASHBOARD ----------
@app.route('/mayor')
def mayor_dashboard():
    # Check if logged in and correct role
    if session.get('user_type', '').lower() == 'mayor':
        
        cursor = db.cursor(dictionary=True)

        # Get all users
        cursor.execute("SELECT user_id, name, email, user_type FROM users")
        users = cursor.fetchall()

        # Get current mayor's name
        cursor.execute("SELECT name FROM users WHERE user_id = %s", (session['user_id'],))
        current_mayor = cursor.fetchone()
        cursor.close()

        # If name is not found, fallback to email
        name = current_mayor['name'] if current_mayor and current_mayor['name'] else session.get('email')

        return render_template('mayor/mayor_dashboard.html', users=users, name=name)

    # Access denied
    flash("Access denied!", "error")
    return redirect(url_for('login'))

#===================admin dashboard===================
@app.route('/admin')
def admin_dashboard():
    # Check if logged in and correct role
    if session.get('user_type', '').lower() == 'admin':
        
        cursor = db.cursor(dictionary=True)

        # Get all users
        cursor.execute("SELECT user_id, name, email, user_type FROM users")
        users = cursor.fetchall()

        # Get current mayor's name
        cursor.execute("SELECT name FROM users WHERE user_id = %s", (session['user_id'],))
        current_admin = cursor.fetchone()
        cursor.close()

        # If name is not found, fallback to email
        name = current_admin['name'] if current_admin and current_admin['name'] else session.get('email')

        return render_template('admin/admin_dashboard.html', users=users, name=name)

    # Access denied
    flash("Access denied!", "error")
    return redirect(url_for('login'))

# ---------- STUDENT DASHBOARD ----------
@app.route('/student')
def student_dashboard():
    if session.get('user_type', '').lower() == 'student':
        cursor = db.cursor(dictionary=True)
        
        # Fetch current student info
        cursor.execute("SELECT name, email FROM users WHERE user_id = %s", (session['user_id'],))
        current_student = cursor.fetchone()
        
        cursor.close()

        # Get student name or email as fallback
        name = current_student['name'] if current_student and current_student['name'] else session['email']
        
        return render_template('student/student_dashboard.html', name=name)

    flash("Access denied!", "error")
    return redirect(url_for('login'))


# ---------- APPLY (NEW SCHOLARSHIP) ----------
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if session.get('user_type', '').lower() != 'student':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    # CHECK IF USER ALREADY HAS AN APPLICATION (for both GET and POST)
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT COUNT(*) as count FROM application 
        WHERE user_id = %s AND (scholarship_type = 'new' OR scholarship_type IS NULL)
    """, (session['user_id'],))
    result = cursor.fetchone()
    
    # If user already applied, redirect them immediately
    if result and result['count'] > 0:
        cursor.close()
        flash("You have already submitted an application. You can only apply once.", "error")
        return redirect(url_for('student_dashboard'))
    
    cursor.close()

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        student_id = request.form.get('student_id')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')
        municipality = request.form.get('municipality')
        barangay = request.form.get('barangay')
        course = request.form.get('course')
        year_level = request.form.get('year_level')
        gwa = request.form.get('gwa')
        reason = request.form.get('reason')

        # Create full name
        full_name = f"{first_name} {middle_name} {last_name}".strip()

        uploaded_files = {}
        for field in ['school_id', 'id_picture', 'birth_certificate', 'grades', 'cor']:
            file = request.files.get(field)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to make it unique
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files[field] = filename
            else:
                uploaded_files[field] = None

        cursor = db.cursor()
        try:
            # DOUBLE CHECK before inserting (in case of race condition)
            cursor.execute("""
                SELECT COUNT(*) as count FROM application 
                WHERE user_id = %s AND (scholarship_type = 'new' OR scholarship_type IS NULL)
            """, (session['user_id'],))
            check_result = cursor.fetchone()
            
            if check_result[0] > 0:
                cursor.close()
                flash("You have already submitted an application. You can only apply once.", "error")
                return redirect(url_for('student_dashboard'))
            
            cursor.execute("""
                INSERT INTO application (
                    user_id, full_name, first_name, middle_name, last_name, student_id, 
                    contact_number, address, municipality, barangay, 
                    course, year_level, gwa, reason, 
                    school_id, id_picture, birth_certificate, grades, cor,
                    scholarship_type, status, submission_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'new', 'Pending', CURRENT_TIMESTAMP)
            """, (
                session['user_id'], full_name, first_name, middle_name, last_name, student_id, 
                contact_number, address, municipality, barangay, 
                course, year_level, gwa, reason,
                uploaded_files['school_id'], uploaded_files['id_picture'],
                uploaded_files['birth_certificate'], uploaded_files['grades'],
                uploaded_files['cor']
            ))
            db.commit()
            flash("✅ Application submitted successfully!", "success")
            return redirect(url_for('student_dashboard'))
        except Exception as e:
            print("Error inserting application:", e)
            db.rollback()
            flash("❌ An error occurred while submitting your application.", "error")
        finally:
            cursor.close()

    return render_template('student/apply.html')


# ---------- RENEW SCHOLARSHIP ----------
@app.route('/renew', methods=['GET', 'POST'])
def renew():
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
            return redirect(url_for('renew'))

    return render_template('student/renew.html')


#==============application===============

@app.route('/my_applications')
def my_applications():
    if session.get('user_type', '').lower() == 'student':
        cursor = db.cursor(dictionary=True)

        # Fetch all applications of the logged-in student
        cursor.execute("""
            SELECT application_id, scholarship_type, submission_date, status
            FROM application
            WHERE user_id = %s
            ORDER BY submission_date DESC
        """, (session['user_id'],))

        applications = cursor.fetchall()
        cursor.close()

        return render_template('student/my_applications.html', applications=applications)
    
    flash("Access denied!", "error")
    return redirect(url_for('login'))

#================mayor_records==================
@app.route('/mayor/records')
def mayor_records():
    # Only mayors are allowed
    if session.get('user_type', '').lower() != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT application_id, user_id, first_name, middle_name, last_name, student_id, address, municipality, baranggay,
               course, year_level, gwa, reason, school_id, id_picture,
               birth_certificate, grades, status, submission_date,
               scholarship_type
        FROM application
        ORDER BY submission_date DESC
    """)
 
    applications = cursor.fetchall()
    cursor.close()

    return render_template('mayor/mayor_records.html', applications=applications)

#==============mayor scholars++++++++++++
@app.route('/mayor/scholars')
def mayor_scholars():
    if session.get('user_type') != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT application_id, user_id, first_name, middle_name, last_name, student_id, address, municipality, baranggay,
               course, year_level, gwa, reason, school_id, id_picture,
               birth_certificate, grades, status, submission_date,
               scholarship_type
        FROM application
        WHERE status = 'Approved'
        ORDER BY submission_date DESC
    """)
    scholars = cursor.fetchall()
    cursor.close()

    return render_template('mayor/mayor_scholars.html', scholars=scholars)

#-----------------pending scholars----------------
@app.route('/mayor/pending')
def mayor_pending():
    if session.get('user_type') != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT application_id, user_id, first_name, middle_name, last_name, student_id, address, municipality, baranggay,
               course, year_level, gwa, reason, school_id, id_picture,
               birth_certificate, grades, status, submission_date,
               scholarship_type
        FROM application
        WHERE status = 'Pending'
        ORDER BY submission_date DESC
    """)
    pending_scholars = cursor.fetchall()
    cursor.close()

    return render_template("mayor/mayor_pending.html", pending_scholars=pending_scholars)

#=============add admin===============
@app.route("/admin/add_admin", methods=["GET", "POST"])
def admin_add_admin():
    if session.get("user_type") != "admin":
        flash("Access denied!", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        name = f"{first_name} {middle_name} {last_name}".strip()

        cursor = db.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing = cursor.fetchone()

        if existing:
            cursor.close()
            return render_template(
                "admin/admin_add_admin.html",
                message="Email already exists!",
                success=False
            )

        # Insert new admin
        cursor.execute("""
            INSERT INTO users (name, email, password, user_type)
            VALUES (%s, %s, %s, 'admin')
        """, (name, email, password))

        db.commit()
        cursor.close()

        return render_template(
            "admin/admin_add_admin.html",
            message="Admin successfully added!",
            success=True
        )

    return render_template("admin/admin_add_admin.html")

#=============add mayor===============
@app.route("/admin/add_mayor", methods=["GET", "POST"])
def admin_add_mayor():
    if session.get("user_type") != "admin":
        flash("Access denied!", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        name = f"{first_name} {middle_name} {last_name}".strip()

        cursor = db.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing = cursor.fetchone()

        if existing:
            cursor.close()
            return render_template(
                "admin/admin_add_mayor.html",
                message="Email already exists!",
                success=False
            )

        # Insert new mayor
        cursor.execute("""
            INSERT INTO users (name, email, password, user_type)
            VALUES (%s, %s, %s, 'mayor')
        """, (name, email, password))

        db.commit()
        cursor.close()

        return render_template(
            "admin/admin_add_mayor.html",
            message="Mayor successfully added!",
            success=True
        )

    return render_template("admin/admin_add_mayor.html")


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


# ================== MAIN ==================
if __name__ == '__main__':
    app.run(debug=True)