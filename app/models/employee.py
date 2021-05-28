from pydantic import BaseModel
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
