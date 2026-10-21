from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()

############################################
#   Employee Method Endpoints
############################################





@router.post("/employee/{employee_id}/methods/askForTimeOff/", response_model=None, tags=["Employee Methods"])
async def execute_employee_askForTimeOff(
    employee_id: int,  # the Employee that askForTimeOff runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the askForTimeOff method on a Employee instance.

    Parameters:
    - startDate: date    - endDate: date    - reason: str    """
    # Employee.askForTimeOff: load the instance
    _employee_object = database.query(Employee).filter(Employee.id == employee_id).first()
    if _employee_object is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Employee.askForTimeOff
    raise HTTPException(
        status_code=501,
        detail="Method 'askForTimeOff' of Employee is modeled but has no implementation - 501, never a fake success",
    )

