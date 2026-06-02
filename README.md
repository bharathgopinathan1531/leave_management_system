# Leave Management System

## Objective
Backend system to manage employees and leave requests.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Features
### Employee Management
- Add Employee
- View Employees
- Get Employee by ID
- Update Employee
- Delete Employee

### Leave Management
- Apply Leave
- View Leave Requests
- Approve Leave
- Reject Leave
- Employee Leave History

### Additional Features
- Search employees by name
- Search employees by department
- Filter leaves by status
- Pagination
- Exception handling
- Swagger documentation

## Run Project

pip install -r requirements.txt

uvicorn main:app --reload

## API Docs

http://127.0.0.1:8000/docs