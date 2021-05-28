from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import date


class EmployeeIn(BaseModel):
    first_name: str
    last_name: str
    position: str
    salary: float
    married: bool
    start_work: date


class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    salary: float
    married: bool
    start_work: date


employees = []


def create_app():
    app = FastAPI()

    @app.get("/")
    def index():
        return {"message": "Hello, World!"}

    @app.get("/employee/", response_model=List[EmployeeIn])
    def read_employees():
        return employees

    @app.post("/employee/", response_model=Employee)
    def add_employee(employee: EmployeeIn):
        employees.append(employee)
        return {**employee.dict(), "id": 1}

    return app
