from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel

from app.models.employee import EmployeeIn, Employee, EmployeeModel, to_json


employee_router = APIRouter()


class ReadEmployeesJson(BaseModel):
    last_name: str = ""
    page: int = 1
    limit: int = 10


class MessageResponse(BaseModel):
    message: str


@employee_router.post("/employee/get_all", response_model=List[Employee])
def read_employees(json: ReadEmployeesJson):
    last_name, page, limit = json.last_name, json.page, json.limit
    employees = EmployeeModel.find_by_last_name(last_name, page, limit)
    return employees


@employee_router.get("/employee/{id}", response_model=Employee)
def get_employee(id: int):
    employee = EmployeeModel.find_by_id(id)
    if not employee:
        raise HTTPException(status_code=404, detail="No such employee")
    return to_json(employee)


@employee_router.post("/employee/", response_model=Employee)
def add_employee(employee: EmployeeIn):
    new_employee = EmployeeModel(employee)
    new_employee.save_to_db()
    return to_json(new_employee)


@employee_router.delete("/employee/{id}", response_model=MessageResponse)
def delete_employee(id: int):
    # make unactive instead of deletion
    result = EmployeeModel.make_unactive_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="No such employee")
    return {"message": "Deleted"}
