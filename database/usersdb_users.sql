CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    password VARCHAR(225),
    name VARCHAR(50),
    user_type VARCHAR(45),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    middle_name VARCHAR(50),
    gender VARCHAR(10),
    bday DATE,
    UNIQUE KEY unique_full_name (first_name, middle_name, last_name)
);