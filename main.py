from schemas import EmployeeCreate,LeaveCreate
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db, SessionLocal
import models
from schemas import EmployeeCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Leave Management System"}


@app.post("/employees")
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    new_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        designation=employee.designation
    )

    db.add(new_employee)
    db.commit()

    return {"message": "Employee Added Successfully"}

@app.get("/employees")
def get_employees(
    name: str = None,
    department: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(models.Employee)

    if name:
        query = query.filter(
            models.Employee.name.contains(name)
        )

    if department:
        query = query.filter(
            models.Employee.department.contains(department)
        )

    return query.offset(skip).limit(limit).all()

@app.get("/employees/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    return employee

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    emp = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not emp:
        return {"message": "Employee not found"}

    emp.name = employee.name
    emp.email = employee.email
    emp.department = employee.department
    emp.designation = employee.designation

    db.commit()

    return {"message": "Employee Updated Successfully"}

@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    emp = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not emp:
        return {"message": "Employee not found"}

    db.delete(emp)
    db.commit()

    return {"message": "Employee Deleted Successfully"}

@app.post("/leaves")
def apply_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db)
):

    employee = db.query(models.Employee).filter(
        models.Employee.id == leave.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
        
    if leave.end_date < leave.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )
            
    existing_leave = db.query(models.Leave).filter(
    models.Leave.employee_id == leave.employee_id,
    models.Leave.start_date <= leave.end_date,
    models.Leave.end_date >= leave.start_date
).first()

    if existing_leave:
        raise HTTPException(
            status_code=400,
            detail="Over lapping leave request not alowed"
            
        )
        
    new_leave = models.Leave(
        employee_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason
    )

    db.add(new_leave)
    db.commit()

    return {
        "message": "Leave Applied Successfully"}

@app.get("/leaves")
def get_leaves(
    status: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(models.Leave)

    if status:
        query = query.filter(
            models.Leave.status == status
        )

    return query.offset(skip).limit(limit).all()


@app.put("/leaves/{leave_id}/approve")
def approve_leave(leave_id: int, db: Session = Depends(get_db)):

    leave = db.query(models.Leave).filter(
        models.Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )
        
    if leave.status == "Approved":
        raise HTTPException(
            status_code=400,
            detail="Approved leave cannot be modified"
        )
    leave.status = "Approved"    

    db.commit()

    return {"message": "Leave Approved"}

@app.put("/leaves/{leave_id}/reject")
def reject_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):
    leave = db.query(models.Leave).filter(
        models.Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,detail="Leave not found"
        )
    
    if leave.status == "Approved":
        raise HTTPException(
            status_code=400,
            detail="Approved leave cannot be modified"
        )

    leave.status = "Rejected"

    db.commit()

    return {"message": "Leave Rejected"}


@app.get("/employees/{employee_id}/leaves")
def employee_leave_history(
    employee_id: int,
    db: Session = Depends(get_db)
):
    leaves = db.query(models.Leave).filter(
        models.Leave.employee_id == employee_id
    ).all()

    return leaves

