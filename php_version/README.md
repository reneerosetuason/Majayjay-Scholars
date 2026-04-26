# Majayjay Scholars - PHP Version

This is the PHP version of the Majayjay Scholars scholarship management system.

## Directory Structure

```
php_version/
├── config/
│   └── database.php          # Database configuration
├── includes/
│   └── session.php           # Session management functions
├── public/
│   ├── index.php             # Home/redirect page
│   ├── login.php             # Login page
│   ├── logout.php            # Logout handler
│   ├── student_dashboard.php # Student dashboard
│   ├── mayor_dashboard.php   # Mayor dashboard
│   └── toggle_renewal.php    # Toggle renewal status
└── uploads/                  # File upload directory
```

## Setup Instructions

### 1. Database Configuration
The system uses the same MySQL database as the Flask version:
- Host: localhost
- User: root
- Password: ren123
- Database: majayjay_scholars

### 2. Web Server Setup

#### Using XAMPP:
1. Copy the `php_version` folder to `C:\xampp\htdocs\`
2. Start Apache from XAMPP Control Panel
3. Access: `http://localhost/php_version/public/`

#### Using PHP Built-in Server:
```bash
cd c:\my_flask_app\php_version\public
php -S localhost:8080
```
Access: `http://localhost:8080/`

### 3. File Upload Permissions
Ensure the `uploads/` directory has write permissions:
```bash
chmod 777 uploads/
```

## Features Implemented

### ✅ Authentication
- Login system with session management
- Role-based access control (Student, Mayor, Admin)
- Logout functionality

### ✅ Student Features
- Student dashboard
- View renewal eligibility based on:
  - Renewal settings (open/closed)
  - Application approval status
- Cannot renew if:
  - No approved application
  - Application is pending
  - Application is rejected

### ✅ Mayor Features
- Mayor dashboard with statistics
- View new applications and renewals
- Toggle renewal form (open/close)
- Real-time status display

### ✅ Session Management
- Secure session handling
- Flash messages for user feedback
- Auto-redirect based on user role

## Login Credentials

### Mayor Account
- Email: mayor@gmail.com
- Password: asdfgh

### Admin Account
- Email: admin@gmail.com
- Password: asdfgh

### Student Accounts
- Email: user1@gmail.com to user50@gmail.com
- Password: asdfgh

## Key Differences from Flask Version

1. **No Email Verification**: PHP version uses simple registration (can be added later)
2. **Session-based**: Uses PHP native sessions instead of Flask sessions
3. **Direct MySQL**: Uses mysqli extension instead of mysql.connector
4. **File Structure**: Follows PHP MVC-like pattern with config/includes/public separation

## Next Steps to Complete

To make this a full replacement of the Flask app, you would need to add:

1. **Registration page** with email verification
2. **Apply for scholarship** form with file uploads
3. **Renew scholarship** form
4. **My Applications** page for students
5. **Mayor Records** page with approve/reject functionality
6. **Mayor Scholars** page
7. **Admin dashboard** with user management
8. **File upload handling** for documents

## Security Notes

⚠️ **Important**: This is a basic implementation. For production use, add:
- Password hashing (use `password_hash()` and `password_verify()`)
- CSRF protection
- Input validation and sanitization
- Prepared statements (already implemented)
- File upload validation
- SQL injection prevention (already using prepared statements)
