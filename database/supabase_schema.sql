-- PostgreSQL Schema for Supabase
-- Run this in Supabase SQL Editor

-- Drop tables in correct order (child tables first)
DROP TABLE IF EXISTS renew CASCADE;
DROP TABLE IF EXISTS application CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create custom types
CREATE TYPE user_type_enum AS ENUM ('student', 'admin', 'mayor');
CREATE TYPE application_status_enum AS ENUM ('pending', 'approved', 'rejected', 'renewal');

-- Create users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type user_type_enum DEFAULT 'student',
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create application table
CREATE TABLE application (
    application_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    student_id VARCHAR(100) UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    contact_number VARCHAR(50),
    address VARCHAR(500),
    municipality VARCHAR(50),
    baranggay VARCHAR(45),
    school_name VARCHAR(255),
    course VARCHAR(255),
    year_level VARCHAR(50),
    gwa DECIMAL(3,2),
    year_applied INT NOT NULL,
    reason TEXT,
    scholarship_type VARCHAR(45),
    school_id VARCHAR(255),
    id_picture VARCHAR(255),
    birth_certificate VARCHAR(255),
    grades VARCHAR(255),
    cor VARCHAR(255),
    status application_status_enum DEFAULT 'pending' NOT NULL,
    archived BOOLEAN DEFAULT FALSE,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create renew table
CREATE TABLE renew (
    renewal_id SERIAL PRIMARY KEY,
    application_id INT NOT NULL,
    user_id INT,
    student_id VARCHAR(100),
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    contact_number VARCHAR(50),
    address VARCHAR(500),
    municipality VARCHAR(50),
    baranggay VARCHAR(45),
    course VARCHAR(255),
    year_level VARCHAR(50),
    gwa DECIMAL(3,2),
    reason TEXT,
    school_id VARCHAR(255),
    id_picture VARCHAR(255),
    birth_certificate VARCHAR(255),
    grades VARCHAR(255),
    cor VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Pending',
    archived BOOLEAN DEFAULT FALSE,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES application(application_id) ON DELETE CASCADE
);

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_application_updated_at BEFORE UPDATE ON application
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_application_user_id ON application(user_id);
CREATE INDEX idx_application_status ON application(status);
CREATE INDEX idx_renew_user_id ON renew(user_id);
CREATE INDEX idx_renew_application_id ON renew(application_id);
