-- =====================================================
-- COMPLETE SCHOLARSHIP DATABASE SCHEMA
-- =====================================================

USE usersdb;

-- Drop existing tables if recreating from scratch
-- WARNING: Uncomment these lines ONLY if you want to delete all data
-- DROP TABLE IF EXISTS application;
-- DROP TABLE IF EXISTS users;

-- =====================================================
-- TABLE: users
-- Stores user account information and personal details
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(225) NOT NULL,
    user_type VARCHAR(45) NOT NULL,
    gender VARCHAR(10),
    bday DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
);

-- =====================================================
-- TABLE: application
-- Stores scholarship application details
-- =====================================================
CREATE TABLE IF NOT EXISTS application (
    -- Primary Key
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Foreign Key to users table
    user_id INT NOT NULL,
    
    -- Student Information
    student_id VARCHAR(100),
    contact_number VARCHAR(50),
    
    -- Personal Information (UNIQUE for foreign key reference)
    first_name VARCHAR(50) NOT NULL UNIQUE,
    last_name VARCHAR(50) NOT NULL UNIQUE,
    middle_name VARCHAR(50) UNIQUE,
    
    -- Address Information (UNIQUE for foreign key reference)
    address VARCHAR(500) UNIQUE,
    municipality VARCHAR(50) UNIQUE,
    baranggay VARCHAR(45) UNIQUE,
    
    -- Academic Information
    school_name VARCHAR(255),
    course VARCHAR(255),
    year_level VARCHAR(50),
    gwa DECIMAL(3,2),
    year_applied INT NOT NULL,
    
    -- Application Details
    reason TEXT,
    scholarship_type VARCHAR(45),
    
    -- Document Uploads (file paths)
    school_id VARCHAR(255),
    id_picture VARCHAR(255),
    birth_certificate VARCHAR(255),
    grades VARCHAR(255),
    cor VARCHAR(255),
    
    -- Application Status and Timestamps
    status ENUM('pending', 'approved', 'rejected', 'renewal') DEFAULT 'pending' NOT NULL,
    archived BOOLEAN DEFAULT FALSE,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraint
    CONSTRAINT fk_user_application 
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    -- Indexes for Performance
    INDEX idx_application_user (user_id),
    INDEX idx_application_status (status),
    INDEX idx_submission_date (submission_date),
    INDEX idx_year_applied (year_applied),
    INDEX idx_school_name (school_name)
);

-- =====================================================
-- FIX EXISTING DATA (if any)
-- =====================================================

-- Disable safe update mode temporarily
SET SQL_SAFE_UPDATES = 0;

-- Fix any NULL or invalid status values
UPDATE application 
SET status = 'pending' 
WHERE status IS NULL 
   OR status NOT IN ('pending', 'approved', 'rejected', 'renewal');

-- Fix any capitalized status values (case-sensitive check)
UPDATE application SET status = 'pending' WHERE BINARY status = 'Pending';
UPDATE application SET status = 'approved' WHERE BINARY status = 'Approved';
UPDATE application SET status = 'rejected' WHERE BINARY status = 'Rejected';
UPDATE application SET status = 'renewal' WHERE BINARY status = 'Renewal';

-- Re-enable safe update mode
SET SQL_SAFE_UPDATES = 1;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Show table structure
SELECT '=== USERS TABLE STRUCTURE ===' AS info;
SHOW COLUMNS FROM users;

SELECT '=== APPLICATION TABLE STRUCTURE ===' AS info;
SHOW COLUMNS FROM application;

-- Check status distribution
SELECT '=== STATUS DISTRIBUTION ===' AS info;
SELECT status, COUNT(*) as count 
FROM application 
GROUP BY status;

-- Show recent applications
SELECT '=== RECENT APPLICATIONS ===' AS info;
SELECT 
    application_id,
    user_id,
    student_id,
    school_name,
    year_applied,
    status,
    scholarship_type,
    submission_date
FROM application 
ORDER BY submission_date DESC 
LIMIT 10;

-- Success message
SELECT '✅ Database schema created/updated successfully!' AS message;
