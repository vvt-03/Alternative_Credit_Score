CREATE DATABASE DB_CREDIT;
USE DB_CREDIT;

-- ADMIN STORE
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
INSERT INTO admins (username, password_hash) 
VALUES ('admin', SHA2('pass123', 256));
SELECT * FROM admins;

CREATE TABLE user_auth (
    email VARCHAR(100) PRIMARY KEY,  
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE user_details (
    aadhar_number VARCHAR(12) PRIMARY KEY,  -- Store hashed Aadhar instead of plain number
    age INT CHECK (age >= 18),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    city VARCHAR(100) NOT NULL DEFAULT 'Unknown',
    email VARCHAR(100) UNIQUE NOT NULL,
    marketing_expense DECIMAL(10,2) DEFAULT 0.00,
    employment_type ENUM('Salaried', 'Self-Employed', 'Unemployed') NOT NULL,
    salary DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (email) REFERENCES user_auth(email) ON DELETE CASCADE
);

CREATE TABLE admin_user_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_history INT DEFAULT 0, 
    on_time_payments DECIMAL(5,2) DEFAULT 0.00,
    credit_utilization DECIMAL(5,2) DEFAULT 0.00,
    utility_bill_payments DECIMAL(10,2) DEFAULT 0.00,
    income_stability DECIMAL(3,2) DEFAULT 0.00,
    debt_to_income_ratio DECIMAL(3,2) DEFAULT 0.00,
    existing_loans INT DEFAULT 0,
    loan_repayment_history INT DEFAULT 0,
    savings DECIMAL(15,2) DEFAULT 0.00,
    aadhar_number VARCHAR(12),
    FOREIGN KEY (aadhar_number) REFERENCES user_details(aadhar_number) ON DELETE CASCADE
);
ALTER TABLE admin_user_details ADD COLUMN bills_paid_on_time INT;
ALTER TABLE admin_user_details 
ADD COLUMN has_credit_card BOOLEAN DEFAULT FALSE;
ALTER TABLE admin_user_details 
ADD COLUMN loans_paid INT DEFAULT 0;
DROP TABLE admin_user_details;
DROP TABLE user_details;
SELECT * FROM user_auth;
SELECT * FROM user_details;
SELECT * FROM admin_user_details;