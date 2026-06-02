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


-- 1. Employees with highest number of leaves
SELECT e.name, COUNT(l.id) AS total_leaves
FROM employees e
JOIN leaves l ON e.id = l.employee_id
GROUP BY e.id, e.name
ORDER BY total_leaves DESC;

-- 2. Department-wise leave count
SELECT e.department, COUNT(l.id) AS leave_count
FROM employees e
JOIN leaves l ON e.id = l.employee_id
GROUP BY e.department;

-- 3. Pending leave requests
SELECT *
FROM leaves
WHERE status = 'Pending';

-- 4. Monthly leave report
SELECT MONTH(start_date) AS month,
       YEAR(start_date) AS year,
       COUNT(*) AS total_leaves
FROM leaves
GROUP BY YEAR(start_date), MONTH(start_date);

-- 5. Employees who never applied for leave
SELECT e.*
FROM employees e
LEFT JOIN leaves l ON e.id = l.employee_id
WHERE l.id IS NULL;

-- 6. Rank employees based on leave count
SELECT
    e.name,
    COUNT(l.id) AS total_leaves,
    RANK() OVER (ORDER BY COUNT(l.id) DESC) AS leave_rank
FROM employees e
LEFT JOIN leaves l ON e.id = l.employee_id
GROUP BY e.id, e.name;