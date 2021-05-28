from fastapi import APIRouter
from typing import List

from app.models.employee import EmployeeIn, Employee


employee_router = APIRouter()
employees = []


@employee_router.get("/employee/", response_model=List[EmployeeIn])
def read_employees():
    return employees


@employee_router.post("/employee/", response_model=Employee)
def add_employee(employee: EmployeeIn):
    employees.append(employee)
    return {**employee.dict(), "id": 1}
