-- LEAVE MANAGEMENT SYSTEM DATABASE

CREATE DATABASE leave_management_db;
USE leave_management_db;

-- EMPLOYEES TABLE
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(100),
    designation VARCHAR(100)
);

-- LEAVES TABLE
CREATE TABLE leaves (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    leave_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    reason VARCHAR(255),
    status VARCHAR(20) DEFAULT 'Pending',

    FOREIGN KEY (employee_id)
    REFERENCES employees(id)
);