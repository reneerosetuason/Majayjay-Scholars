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
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')  # Optional field
        last_name = request.form.get('last_name')
        email_verified = request.form.get('email_verified')

        # Validate required fields (middle_name is optional)
        if not all([email, password, confirm, first_name, last_name]):
            flash("Please fill out all required fields.", "error")
            return redirect(url_for('register'))

        # Check if email is verified
        if email_verified != 'true' or not is_email_verified(email):
            flash('Please verify your email before registering', 'error')
            return redirect(url_for('register'))

        # Check password match
        if password != confirm:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))

        cursor = db.cursor()

        try:
            # Hash the password before storing (recommended!)
            # If you have werkzeug.security: hashed_password = generate_password_hash(password)
            
            cursor.execute("""
                INSERT INTO users (email, password, first_name, middle_name, last_name, user_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (email, password, first_name, middle_name, last_name, 'student'))
            db.commit()
            
            # Clean up verification data after successful registration
            cleanup_verification(email)
            
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash("Email already exists!", "error")
            return redirect(url_for('register'))
        except Exception as e:
            db.rollback()
            flash(f"Registration failed: {str(e)}", "error")
            return redirect(url_for('register'))
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
    if session.get('user_type', '').lower() != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))
    
    cursor = db.cursor(dictionary=True)
    
    # Get mayor's name
    cursor.execute("SELECT first_name, last_name FROM users WHERE user_id = %s", (session['user_id'],))
    mayor = cursor.fetchone()
    name = f"{mayor['first_name']} {mayor['last_name']}" if mayor else session.get('email')
    
    # Get all active applications (exclude archived)
    cursor.execute("""
        SELECT scholarship_type, status 
        FROM application 
        WHERE archived = FALSE OR archived IS NULL
    """)
    applications = cursor.fetchall()
    cursor.close()
    
    # Separate by type
    new_apps = [a for a in applications if a['scholarship_type'] == 'new']
    renewals = [a for a in applications if a['scholarship_type'] == 'renewal']
    
    return render_template('mayor/mayor_dashboard.html', 
                         name=name, 
                         new_applications=new_apps, 
                         renewals=renewals)

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
        cursor.execute("SELECT first_name FROM users WHERE user_id = %s", (session['user_id'],))
        current_student = cursor.fetchone()
        
        cursor.close()

        # Get student name or email as fallback
        first_name = current_student['first_name'] if current_student and current_student.get('first_name') else session.get('email', 'Student')
        
        return render_template('student/student_dashboard.html', first_name=first_name)

    flash("Access denied!", "error")
    return redirect(url_for('login'))


# ---------- APPLY (NEW SCHOLARSHIP) ----------
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if session.get('user_type', '').lower() != 'student':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    # Get user information from users table
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT first_name, middle_name, last_name, email 
        FROM users 
        WHERE user_id = %s
    """, (session['user_id'],))
    user_info = cursor.fetchone()
    
    if not user_info:
        cursor.close()
        flash("User information not found!", "error")
        return redirect(url_for('login'))

    # CHECK IF USER ALREADY HAS AN APPLICATION
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
        # Get form data
        student_id = request.form.get('student_id')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')
        municipality = request.form.get('municipality')
        barangay = request.form.get('barangay')
        school_name = request.form.get('school_name')
        course = request.form.get('course')
        year_level = request.form.get('year_level')
        gwa = request.form.get('gwa')
        year_applied = request.form.get('year_applied')
        reason = request.form.get('reason')

        # Handle file uploads
        uploaded_files = {}
        for field in ['school_id', 'id_picture', 'birth_certificate', 'grades', 'cor']:
            file = request.files.get(field)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
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
            # Check if user already has an application
            cursor.execute("""
                SELECT COUNT(*) as count FROM application 
                WHERE user_id = %s
            """, (session['user_id'],))
            check_result = cursor.fetchone()
            
            if check_result[0] > 0:
                cursor.close()
                flash("You have already submitted an application. You can only apply once.", "error")
                return redirect(url_for('student_dashboard'))
            
            # Insert application with all fields
            cursor.execute("""
                INSERT INTO application (
                    user_id, student_id, contact_number, address, 
                    municipality, baranggay, school_name, course, year_level, 
                    gwa, year_applied, reason, school_id, id_picture, 
                    birth_certificate, grades, cor, scholarship_type
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, 'new'
                )
            """, (
                session['user_id'], student_id, contact_number, address,
                municipality, barangay, school_name, course, year_level,
                gwa, year_applied, reason, uploaded_files['school_id'], 
                uploaded_files['id_picture'], uploaded_files['birth_certificate'],
                uploaded_files['grades'], uploaded_files['cor']
            ))
            db.commit()
            
            flash("✅ Application submitted successfully!", "success")
            return redirect(url_for('student_dashboard'))
        except Exception as e:
            print("Error inserting application:", e)
            import traceback
            traceback.print_exc()
            db.rollback()
            flash("❌ An error occurred while submitting your application. Please try again.", "error")
        finally:
            cursor.close()

    # Pass user_info to template for pre-filling the form
    return render_template('student/apply.html', user_info=user_info)

# ---------- RENEW SCHOLARSHIP ----------
@app.route('/renew', methods=['GET', 'POST'])
def renew():
    if session.get('user_type', '').lower() != 'student':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    # Check if user already submitted a renewal
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT COUNT(*) as count FROM renew WHERE user_id = %s
    """, (session['user_id'],))
    renewal_check = cursor.fetchone()
    
    if renewal_check and renewal_check['count'] > 0:
        cursor.close()
        flash("You have already submitted a renewal application.", "error")
        return redirect(url_for('student_dashboard'))
    
    # Fetch existing application data for autofill
    cursor.execute("""
        SELECT a.first_name, a.middle_name, a.last_name, a.address, 
               a.municipality, a.baranggay, a.application_id
        FROM application a
        WHERE a.user_id = %s
        ORDER BY a.submission_date DESC
        LIMIT 1
    """, (session['user_id'],))
    app_data = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        try:
            user_id = session.get('user_id')

            first_name = request.form.get('first_name')
            middle_name = request.form.get('middle_name')
            last_name = request.form.get('last_name')
            student_id = request.form.get('student_id')
            contact_number = request.form.get('contact_number')
            address = request.form.get('address')
            baranggay = request.form.get('baranggay')
            municipality = request.form.get('municipality')
            course = request.form.get('course')
            year_level = request.form.get('year_level')
            gwa = request.form.get('gwa')
            reason = request.form.get('reason')
            first_name = request.form.get('first_name')
            middle_name = request.form.get('middle_name')
            last_name = request.form.get('last_name')

            uploaded_files = {}
            for field in ['school_id', 'id_picture', 'birth_certificate', 'grades', 'cor']:
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
                INSERT INTO renew (
                    renewal_id, application_id, user_id, student_id, contact_number, 
                    address, baranggay, municipality,
                    course, year_level, gwa, reason,
                    school_id, id_picture, birth_certificate, grades, cor,
                    first_name, middle_name, last_name,
                    status, submission_date
                ) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending', NOW())
            """, (
                request.form.get('application_id'), user_id, student_id, contact_number,
                address, baranggay, municipality,
                course, year_level, gwa, reason,
                uploaded_files['school_id'], uploaded_files['id_picture'],
                uploaded_files['birth_certificate'], uploaded_files['grades'], uploaded_files['cor'],
                first_name, middle_name, last_name
            ))

            db.commit()
            cursor.close()
            flash("✅ Renewal application submitted successfully!", "success")
            return redirect(url_for('student_dashboard'))

        except Exception as e:
            print("Error submitting renewal application:", e)
            import traceback
            traceback.print_exc()
            flash("❌ Error submitting renewal application. Please try again.", "error")
            return redirect(url_for('renew'))

    if not app_data:
        flash("No previous application found. Please apply first.", "error")
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/renew.html', app_data=app_data)


#==============application===============

@app.route('/my_applications')
def my_applications():
    if session.get('user_type', '').lower() != 'student':
        flash("Access denied!", "error")
        return redirect(url_for('login'))
    
    cursor = db.cursor(dictionary=True)

    # Fetch all applications with user details via JOIN
    # This gets ALL columns from application table AND name fields from users table
    cursor.execute("""
        SELECT 
            a.application_id,
            a.user_id,
            a.student_id,
            a.contact_number,
            a.address,
            a.municipality,
            a.baranggay,
            a.course,
            a.year_level,
            a.gwa,
            a.reason,
            a.scholarship_type,
            a.school_id,
            a.id_picture,
            a.birth_certificate,
            a.grades,
            a.cor,
            a.status,
            a.submission_date,
            a.updated_at,
            u.first_name,
            u.middle_name,
            u.last_name,
            u.email
        FROM application a
        INNER JOIN users u ON a.user_id = u.user_id
        WHERE a.user_id = %s
        ORDER BY a.submission_date DESC
    """, (session['user_id'],))

    applications = cursor.fetchall()
    cursor.close()

    return render_template('student/my_applications.html', applications=applications)

#================mayor_records==================
@app.route('/mayor/records')
def mayor_records():
    # Only mayors are allowed
    if session.get('user_type', '').lower() != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    show_archived = request.args.get('archived', 'false').lower() == 'true'
    cursor = db.cursor(dictionary=True)

    # JOIN application with users table to get name fields
    if show_archived:
        where_clause = "WHERE a.archived = TRUE"
    else:
        where_clause = "WHERE a.archived = FALSE OR a.archived IS NULL"

    cursor.execute(f"""
        SELECT 
            a.application_id,
            a.user_id,
            a.student_id,
            a.contact_number,
            a.address,
            a.municipality,
            a.baranggay,
            a.school_name,
            a.course,
            a.year_level,
            a.gwa,
            a.year_applied,
            a.reason,
            a.scholarship_type,
            a.school_id,
            a.id_picture,
            a.birth_certificate,
            a.grades,
            a.cor,
            a.status,
            a.archived,
            a.submission_date,
            a.updated_at,
            u.first_name,
            u.middle_name,
            u.last_name,
            u.email
        FROM application a
        INNER JOIN users u ON a.user_id = u.user_id
        {where_clause}
        ORDER BY a.submission_date DESC
    """)
 
    applications = cursor.fetchall()
    cursor.close()

    return render_template('mayor/mayor_records.html', applications=applications, show_archived=show_archived)

#================archive application==================
@app.route('/mayor/archive/<int:application_id>', methods=['POST'])
def archive_application(application_id):
    if session.get('user_type', '').lower() != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE application 
            SET archived = TRUE 
            WHERE application_id = %s
        """, (application_id,))
        db.commit()
        flash("Application archived successfully!", "success")
    except Exception as e:
        print(f"Error archiving application: {e}")
        db.rollback()
        flash("Error archiving application.", "error")
    finally:
        cursor.close()
    
    return redirect(url_for('mayor_records'))

#================approve application==================
@app.route('/mayor/approve/<int:application_id>', methods=['POST'])
def approve_application(application_id):
    if session.get('user_type', '').lower() != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE application 
            SET status = 'approved' 
            WHERE application_id = %s
        """, (application_id,))
        db.commit()
        flash("Application approved successfully!", "success")
    except Exception as e:
        print(f"Error approving application: {e}")
        db.rollback()
        flash("Error approving application.", "error")
    finally:
        cursor.close()
    
    return redirect(url_for('mayor_records'))

#================reject application==================
@app.route('/mayor/reject/<int:application_id>', methods=['POST'])
def reject_application(application_id):
    if session.get('user_type', '').lower() != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE application 
            SET status = 'rejected' 
            WHERE application_id = %s
        """, (application_id,))
        db.commit()
        flash("Application rejected.", "info")
    except Exception as e:
        print(f"Error rejecting application: {e}")
        db.rollback()
        flash("Error rejecting application.", "error")
    finally:
        cursor.close()
    
    return redirect(url_for('mayor_records'))
#==============mayor scholars++++++++++++
@app.route('/mayor/scholars')
def mayor_scholars():
    if session.get('user_type') != 'mayor':
        flash("Access denied!", "error")
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            a.application_id,
            a.user_id,
            a.student_id,
            a.address,
            a.municipality,
            a.baranggay,
            a.school_name,
            a.course,
            a.year_level,
            a.gwa,
            a.year_applied,
            a.reason,
            a.school_id,
            a.id_picture,
            a.birth_certificate,
            a.grades,
            a.status,
            a.submission_date,
            a.scholarship_type,
            u.first_name,
            u.middle_name,
            u.last_name,
            u.email
        FROM application a
        INNER JOIN users u ON a.user_id = u.user_id
        WHERE a.status = 'approved' AND (a.archived = FALSE OR a.archived IS NULL)
        ORDER BY a.submission_date DESC
    """)
    scholars = cursor.fetchall()
    cursor.close()

    return render_template('mayor/mayor_scholars.html', scholars=scholars)


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