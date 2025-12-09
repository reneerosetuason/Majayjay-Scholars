-- Drop tables in correct order
DROP TABLE IF EXISTS renew CASCADE;
DROP TABLE IF EXISTS application CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    contact_number VARCHAR(20),
    password VARCHAR(255),
    user_type VARCHAR(20) CHECK (user_type IN ('student', 'admin', 'mayor')) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create application table (user_id changed to INT to match users.user_id)
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
    status VARCHAR(20) CHECK (status IN ('pending', 'approved', 'rejected', 'renewal')) DEFAULT 'pending' NOT NULL,
    archived BOOLEAN DEFAULT FALSE,
    submission_date TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create renew table (user_id changed to INT)
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
    submission_date TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (application_id) REFERENCES application(application_id) ON DELETE CASCADE
);

-- Enable RLS
ALTER TABLE "public"."users" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."application" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."renew" ENABLE ROW LEVEL SECURITY;

-- Users policies (allow authenticated users to insert/read/update)
CREATE POLICY "Enable insert for authenticated" ON "public"."users"
FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Enable read for authenticated" ON "public"."users"
FOR SELECT TO authenticated USING (true);

CREATE POLICY "Enable update for authenticated" ON "public"."users"
FOR UPDATE TO authenticated USING (true) WITH CHECK (true);

-- Application policies
CREATE POLICY "Enable all for application" ON "public"."application"
FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Renew policies
CREATE POLICY "Enable all for renew" ON "public"."renew"
FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Drop existing policy
DROP POLICY IF EXISTS "Enable insert for authenticated" ON "public"."users";

-- Create new policy allowing both anon and authenticated to insert
CREATE POLICY "Enable insert for registration" ON "public"."users"
FOR INSERT WITH CHECK (true);
