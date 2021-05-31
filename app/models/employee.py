from .database import base, session
from datetime import date
from paginate_sqlalchemy import SqlalchemyOrmPage
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Float, Boolean, Date


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    position: str
    salary: float
    married: bool
    start_work: date


class EmployeeIn(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    active: bool


def to_json(x):
    return {
        'id': x.id,
        'first_name': x.first_name,
        'last_name': x.last_name,
        'position': x.position,
        'salary': x.salary,
        'married': x.married,
        'start_work': x.start_work,
        'active': x.active
    }


class EmployeeModel(base):
    __tablename__ = 'employees'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String(55))
    last_name = Column(String(55))
    position = Column(String(255))
    salary = Column(Float())
    married = Column(Boolean())
    start_work = Column(Date())
    active = Column(Boolean())

    def __init__(self, employee):
        self.first_name = employee.first_name
        self.last_name = employee.last_name
        self.position = employee.position
        self.salary = employee.salary
        self.married = employee.married
        self.start_work = employee.start_work
        self.active = True

    @classmethod
    def find_by_last_name(cls, last_name, page, limit):
        employees = session.query(cls).filter(
            EmployeeModel.last_name.like(f"%{last_name}%"))
        if employees:
            employees = SqlalchemyOrmPage(employees, page, limit).items
        return list(map(lambda x: to_json(x), employees))

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def make_unactive_by_id(cls, id):
        employee = EmployeeModel.find_by_id(id)
        if not employee or not employee.active:
            return False
        employee.active = False
        session.commit()
        return True

    @classmethod
    def delete_by_id(cls, id):
        employee = EmployeeModel.find_by_id(id)
        session.delete(employee)
        session.commit()

    def save_to_db(self):
        session.add(self)
        session.commit()
